import os
from typing import Final

LOGGING_LEVEL: Final[str] = os.getenv("LOGGING_LEVEL", "INFO").upper()

DEBUG_SQLALCHEMY: Final[bool] = os.getenv("DEBUG_SQLALCHEMY", "false").lower() == "true"
DEBUG_FASTAPI: Final[bool] = os.getenv("DEBUG_FASTAPI", "false").lower() == "true"

DATA_PATH: Final[str] = os.getenv("DATA_PATH", "data")
DATABASE_URL: Final[str] = os.getenv("DATABASE_URL", "sqlite:///./database.sqlite")

CORS_ALLOW_ORIGIN: Final[str] = os.getenv("CORS_ALLOW_ORIGIN", "*")
CORS_ALLOW_METHOD: Final[str] = os.getenv("CORS_ALLOW_METHOD", "*")
CORS_ALLOW_HEADER: Final[str] = os.getenv("CORS_ALLOW_HEADER", "*")
