from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    # MLS Configuration
    MLS_URL: Optional[str] = None
    MLS_AUTHTOKEN: Optional[str] = None
    
    # Supabase Configuration
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    # Resource Record Key Mapping
    RESOURCE_RECORD_KEY_MAPPING: Dict[str, str] = {}
    
    # JWT Configuration
    JWT_SECRET_KEY: Optional[str] = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 