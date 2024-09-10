import os
from structlog import get_logger
from salestrack.core.config import Settings

logger = get_logger(__name__)


def get_app_settings() -> Settings:
    environ = os.getenv("APP_ENVIRON", "dev")
    return Settings(_env_file=f"{environ}.env", environment=environ)