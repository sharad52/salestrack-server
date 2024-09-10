from pydantic import Field, SecretStr
from salestrack.core.common import SettingsModelBase


class DatabaseSettings(SettingsModelBase):
    host: str = Field(validation_alias="HOST")
    port: int = Field(validation_alias="PORT")
    user: str = Field(validation_alias="USER")
    dbname: str = Field(validation_alias="DBNAME")
    password: str = Field(validation_alias="PASSWORD")