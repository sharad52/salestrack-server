""" """

from pydantic import Field, SecretBytes
from salestrack.core.common import SettingsModelBase


class JWTSettings(SettingsModelBase):
    secret_key: SecretBytes = Field(alias="SECRET_KEY")
    access_token_ttl_seconds: int  = Field(alias="ACCESS_TOKEN_TTL_SECONDS")
    refresh_token_ttl_seconds: int = Field(alias="REFRESH_TOKEN_TTL_SECONDS")