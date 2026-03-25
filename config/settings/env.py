import os
import signal
import types
from pathlib import Path
from urllib.parse import parse_qs, urlparse


class Env:
    """Typed access to environment variables."""

    @staticmethod
    def get_str(key: str, default: str = "") -> str:
        return os.environ.get(key, default)

    @staticmethod
    def require(key: str) -> str:
        """Get a required environment variable, raising if unset or empty."""
        val = os.environ.get(key, "")
        if not val:
            raise ValueError(f"Required environment variable {key} is not set")
        return val

    @staticmethod
    def get_bool(key: str, *, default: bool = False) -> bool:
        return Env.get_str(key, str(default)).lower() in ("true", "1", "yes")

    @staticmethod
    def get_int(key: str, *, default: int = 0) -> int:
        val = Env.get_str(key, str(default))
        try:
            return int(val)
        except ValueError:
            raise ValueError(f"Environment variable {key} must be an integer, got: {val!r}") from None

    @staticmethod
    def get_list(key: str, *, default: str = "", sep: str = ",") -> list[str]:
        val = Env.get_str(key, default)
        return [item.strip() for item in val.split(sep) if item.strip()] if val else []

    @staticmethod
    def database_url(key: str = "DATABASE_URL", default: str = "sqlite:///db.sqlite3") -> dict[str, object]:
        """Parse a DATABASE_URL into a Django DATABASES entry."""
        url = Env.get_str(key, default)
        if not url:
            raise ValueError(f"Environment variable {key} is empty — provide a valid database URL")
        if url.startswith("sqlite"):
            return {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": url.split("///", 1)[1] if "///" in url else ":memory:",
            }
        parsed = urlparse(url)
        pg_schemes = {"postgres", "postgresql", "postgis"}
        if parsed.scheme not in pg_schemes and not parsed.scheme.startswith(("postgres+", "postgresql+")):
            raise ValueError(
                f"Unsupported DATABASE_URL scheme '{parsed.scheme}' — "
                f"only sqlite and PostgreSQL (postgres://, postgresql://) are supported"
            )
        options = parse_qs(parsed.query)
        db: dict[str, object] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": parsed.path.lstrip("/"),
            "USER": parsed.username or "",
            "PASSWORD": parsed.password or "",
            "HOST": parsed.hostname or "localhost",
            "PORT": parsed.port or 5432,
        }
        sslmode = options.get("sslmode", ["require"])[0]
        db["OPTIONS"] = {"sslmode": sslmode}
        return db

    @staticmethod
    def load_dotenv(path: Path) -> None:
        """Load a .env file into os.environ (setdefault, no overwrite)."""
        if not path.is_file():
            return
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                os.environ.setdefault(key.strip(), value)


class GracefulShutdown:
    """Signal handler for graceful worker shutdown."""

    should_stop: bool = False

    @classmethod
    def register(cls) -> None:
        cls.should_stop = False
        signal.signal(signal.SIGTERM, cls._handle)
        signal.signal(signal.SIGINT, cls._handle)

    @classmethod
    def _handle(cls, signum: int, frame: types.FrameType | None) -> None:
        cls.should_stop = True
