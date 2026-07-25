from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url : str
    secret_key: str
    r2_access_key_id: str
    r2_secret_access_key: str
    r2_endpoint_url: str
    r2_bucket_name: str
    r2_public_url: str
    class Config:
        env_file = ".env"

settings = Settings()