import logging
import logging.config

# Konfiguracja logowania
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "INFO",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

# Ustaw logowanie przy imporcie pakietu
logging.config.dictConfig(LOGGING_CONFIG)

# Wskazówka: możesz zdefiniować domyślnego loggera, jeśli to konieczne
logger = logging.getLogger(__name__)
logger.debug("Logging configured in __init__.py")
