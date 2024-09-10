""" """
from pydantic import Field
from typing import Any, List, Optional, Union
from pydantic_settings import SettingsConfigDict
from pydantic import AnyHttpUrl, PostgresDsn, field_validator, ValidationInfo
from salestrack.core.common import BaseSettings, APPEnvironment
from salestrack.core.jwt import JWTSettings
from salestrack.core.db import DatabaseSettings


class Settings(BaseSettings):
    environment: APPEnvironment = Field(default=APPEnvironment.production)
    jwt: JWTSettings = Field(validation_alias="JWT")
    db: DatabaseSettings = Field(validation_alias="DB")

    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: Union[List[AnyHttpUrl], List[str]] = []
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=True
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_originals(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Union[Optional[PostgresDsn], str] = None

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            path=f"/{values.data.get('POSTGRES_DB') or ''}",
        )
    
    #JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    
    #for testcase
    TEST_DB_URI: Union[Optional[PostgresDsn], str] = None

settings = Settings()
