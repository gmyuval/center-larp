import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse


class Env:
    """Typed access to environment variables."""

    @staticmethod
    def str(key: str, default: str = "") -> str:
        return os.environ.get(key, default)

    @staticmethod
    def bool(key: str, *, default: bool = False) -> bool:
        return Env.str(key, str(default)).lower() in ("true", "1", "yes")

    @staticmethod
    def int(key: str, *, default: int = 0) -> int:
        return int(Env.str(key, str(default)))

    @staticmethod
    def list(key: str, *, default: str = "", sep: str = ",") -> list[str]:
        val = Env.str(key, default)
        return [item.strip() for item in val.split(sep) if item.strip()] if val else []

    @staticmethod
    def database_url(key: str = "DATABASE_URL", default: str = "sqlite:///db.sqlite3") -> dict[str, object]:
        """Parse a DATABASE_URL into a Django DATABASES entry."""
        url = Env.str(key, default)
        if url.startswith("sqlite"):
            return {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": url.split("///", 1)[1] if "///" in url else ":memory:",
            }
        parsed = urlparse(url)
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
                os.environ.setdefault(key.strip(), value.strip())
