from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    database_name: str
    jwt_secret: str
    algorithm: str
    jwt_token_time_minuites: str

    class Config:
        env_file = ".env"
