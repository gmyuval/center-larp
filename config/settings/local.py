from pathlib import Path

from .env import Env

Env.load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

from .base import *  # noqa: E402, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]
