import os
import sys
import typing
from pathlib import Path
from yaml import safe_load
from structlog import get_logger
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ValidationError

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
    pg_schema: str = "public"
    pg_min_size: int = 5
    pg_max_size: int = 10
    pg_use_ssl: bool = True

    class Config: 
        """env_prefix should be defined by child Settings"""
        env_file = "production.env"


def _load_config(
    app_env: str, config_dir: Path
) -> typing.Dict[typing.Any, typing.Any]:
    """load config file"""
    config_file = config_dir.joinpath(f"{app_env}.yaml")
    if not config_file.exists():
        raise ValueError(f"Config file {config_file} doesn't exists")
    logger.info("Found Configuration ... %s", config_file)
    return safe_load(open(config_file, "r").read())


def settings_factory(
    settings_class: typing.Type[CoreSettings], env_prefix: str, base_path: Path
) -> CoreSettings:
    """generate settings object using provided class"""
    app_env = os.getenv(env_prefix + "APP_ENV", "production")
    config_dir = base_path.joinpath("config")
    try: 
        settings = settings_class(
            _env_file=f"{app_env}.env",
            base_path=base_path,
            app_env=app_env,
            **_load_config(app_env, config_dir),
        )
    except ValidationError as e:
        logger.error("Invalid Config/Settings.")
        logger.exception(e)
        sys.exit(-1)
    else:
        return settings