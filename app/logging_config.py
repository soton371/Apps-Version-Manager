import logging
import logging.config
from pathlib import Path
from .config import settings

# Base directory for logs
BASE_DIR = Path(__file__).resolve().parent

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(pathname)s:%(lineno)d]",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "app.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "app": {
            "handlers": ["console", "file"],
            "level": "DEBUG",  # Change to "INFO" for production
            "propagate": False,
        },
    },
}





# Adjust logging levels based on environment
if settings.env_mood == "production":
    LOGGING_CONFIG["handlers"]["console"]["level"] = "WARNING"
    LOGGING_CONFIG["loggers"]["app"]["level"] = "INFO"

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")


