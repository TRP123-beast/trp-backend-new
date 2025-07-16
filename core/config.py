
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # MLS API Configuration
    MLS_URL: str
    MLS_AUTHTOKEN: str
    MLS_PROPERTY_TYPE: str
    MLS_RENTAL_APPLICATION: str
    MLS_ORIFINATING_SYSTEM_NAME: str
    MLS_TOP_LIMIT: str
    MLS_PPROPERTY_FILTER_FIELDS: str
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings() 