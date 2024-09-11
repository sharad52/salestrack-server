# from typing import Any, Dict, List, Optional, Union
# from pydantic import AnyHttpUrl, PostgresDsn, field_validator, ValidationInfo
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     PROJECT_NAME: str
#     BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], List[str]] = []
    
#     model_config = SettingsConfigDict(
#         env_file=".env", 
#         case_sensitive=True
#     )

#     @field_validator("BACKEND_CORS_ORIGINS", mode="before")
#     def assemble_cors_originals(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
#         if isinstance(v, str) and not v.startswith("["):
#             return [i.strip() for i in v.split(",")]
#         elif isinstance(v, (list, str)):
#             return v
#         raise ValueError(v)
    
#     POSTGRES_SERVER: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#     DATABASE_URI: Union[Optional[PostgresDsn], str] = None

#     @field_validator("DATABASE_URI", mode="before")
#     def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
#         if isinstance(v, str):
#             return v
#         return PostgresDsn.build(
#             scheme="postgresql",
#             username=values.data.get("POSTGRES_USER"),
#             password=values.data.get("POSTGRES_PASSWORD"),
#             host=values.data.get("POSTGRES_SERVER"),
#             path=f"/{values.data.get('POSTGRES_DB') or ''}",
#         )
    
#     #JWT
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#     REFRESH_TOKEN_EXPIRE_MINUTES: int
#     ALGORITHM: str
#     JWT_SECRET_KEY: str
#     JWT_REFRESH_SECRET_KEY: str
    
#     #for testcase
#     TEST_DB_URI: Union[Optional[PostgresDsn], str] = None

# settings = Settings()

import typing
from pathlib import Path
from functools import lru_cache
from salestrack_utils.salestrack.core.settings import CoreSettings, settings_factory


ENV_PREFIX = "SALESTRACK_"
APP_PATH = Path(__file__).parent
BASE_PATH = APP_PATH.parent
API_BASE_VERSION = "V1"


class AppSettings(CoreSettings):
    app_id: str = "com.salestrack.api"
    app_name: str = "salestrackapi"

    class Config:
        env_prefix = ENV_PREFIX


@lru_cache
def get_application_settings(env_prefix=ENV_PREFIX, base_path=BASE_PATH):
    return settings_factory(
        settings_class=AppSettings,
        env_prefix=env_prefix,
        base_path=base_path
    )

