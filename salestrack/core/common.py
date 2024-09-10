from enum import StrEnum
from structlog import get_logger
from pydantic import BaseModel, ConfigDict
from pydantic_settings import SettingsConfigDict
from pydantic_settings import BaseSettings as PydanticBaseSettings

logger = get_logger(__name__)


class APPEnvironment(StrEnum):
    # setting var name for different environments
    production = "production"
    staging = "staging"
    testing = "testing"
    develop = "dev"

    def is_testing(self):
        logger.debug("What am I", self=self)


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
    )


class SettingsModelBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")