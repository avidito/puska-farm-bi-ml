import json
from pydantic import Field, SecretStr, field_serializer
from pydantic_settings import BaseSettings
from beam_nuggets.io import relational_db


# Getter
def get_connection(conn_id: str):
    conn = {
        "ops-db": CONFIG_OPS_DATABASE,
        "dwh-db": CONFIG_DWH_DATABASE
    }.get(conn_id)
    if (conn):
        return conn
    else:
        raise ValueError(f"No connection defined for '{conn_id}'")

# Connection List
class ConfigOPSDatabase(BaseSettings):
    host: str = Field(alias="ops_db_hostname")
    port: int = Field(alias="ops_db_port")
    database: str = Field(alias="ops_db_name")
    username: str = Field(alias="ops_db_user")
    password: SecretStr = Field(alias="ops_db_password")

    @field_serializer('password', when_used='json')
    def dump_secret(self, v: SecretStr):
        return v.get_secret_value()

CONFIG_OPS_DATABASE = relational_db.SourceConfiguration(**{
    "drivername": "postgresql",
    **json.loads(ConfigOPSDatabase().model_dump_json())
})

class ConfigDWHDatabase(BaseSettings):
    host: str = Field(alias="dwh_db_hostname")
    port: int = Field(alias="dwh_db_port")
    database: str = Field(alias="dwh_db_name")
    username: str = Field(alias="dwh_db_user")
    password: SecretStr = Field(alias="dwh_db_password")

    @field_serializer('password', when_used='json')
    def dump_secret(self, v: SecretStr):
        return v.get_secret_value()

CONFIG_DWH_DATABASE = relational_db.SourceConfiguration(**{
    "drivername": "postgresql",
    **json.loads(ConfigDWHDatabase().model_dump_json())
})