from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    db_host: str
    db_name: str
    db_port: str
    db_user: str
    db_pwd: SecretStr