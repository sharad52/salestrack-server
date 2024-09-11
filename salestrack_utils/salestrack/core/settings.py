import typing
from pathlib import Path
from structlog import get_logger
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn

logger = get_logger("__name__")


class CoreSettings(BaseSettings):
    """Core Settings for Salestrack"""
    app_id: str
    app_name: str
    base_path: Path

    #runtime information
    app_env: typing.Literal["development", "testing", "production"]
    debug: bool
    is_testing: bool = False

    #alembic specific
    components: typing.List[str]

    #postgres Settings
    pg_dsn: PostgresDsn
    pg_min_size: int = 5
    pg_max_size: int = 10
    pg_use_ssl: bool = True

    class Config: 
        """env_prefix should be defined by child Settings"""
        env_file = "production.env"