
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # MLS API Configuration
    MLS_URL: str
    MLS_AUTHTOKEN: str
    MLS_PROPERTY_TYPE: str
    MLS_RENTAL_APPLICATION: str
    MLS_ORIFINATING_SYSTEM_NAME: str
    MLS_TOP_LIMIT: str
    MLS_PPROPERTY_FILTER_FIELDS: str
    MLS_PROPERTY_IMAGE_FILTER_FIELDS: str
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # JWT Configuration (alternative names used in some files)
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() 