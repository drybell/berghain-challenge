from pydantic import BaseModel, UUID4, AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from ipaddress import IPv4Address as IPv4

class MyPlayerConfig(BaseModel):
    id       : UUID4
    email    : str
    username : str

class ServerConfig(BaseModel):
    host : IPv4
    port : int

class GameConfig(BaseModel):
    url : AnyUrl

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env'
        , env_nested_delimiter="_"
        , env_prefix="BASE_"
    )

    game   : GameConfig
    server : ServerConfig
    player : MyPlayerConfig
