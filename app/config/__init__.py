import os 
from pydantic import BaseModel, field_serializer
from pydantic_settings import BaseSettings
from typing import List, Optional, Literal, Union
from dotenv import load_dotenv
import datetime as dt
from app.utils.logger import log

EnvType = Literal['local', 'dev', 'prod']

class Settings(BaseSettings):
    app_name: Optional[str] = 'RAG Demo'
    author: Optional[str] = 'Hadi Honarvar Nazari'
    environment: Optional[str] = 'local'
    
    ENV: Optional[str] = 'local'
    
    FASTAPI_HOST: Optional[str] = ''
    FASTAPI_PORT: Optional[str] = ''
    
    cors_origins: Optional[str] = ''
    cors_methods: Optional[str] = ''
    cors_headers: Optional[str] = ''
    
    DB_QDRANT_NAME: Optional[str] = ''
    DB_QDRANT_HOST: Optional[str] = ''
    DB_QDRANT_PORT: Optional[str] = ''
    DB_QDRANT_USER: Optional[str] = ''
    DB_QDRANT_PASSWORD: Optional[str] = ''
    DB_QDRANT_API_URL: Optional[str] = ''
    DB_QDRANT_API_KEY: Optional[str] = ''
    
    OPENAI_API_KEY: Optional[str] = ''
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        
    @field_serializer("FASTAPI_HOST", when_used='always')
    def encode_fastapi_host(self, value: Optional[str]) -> str:
        return value or ''
    
    @field_serializer("cors_origins", when_used='always')
    def encode_cors_origins(self, value: Optional[str]) -> str:
        return value or ''
    
    @field_serializer("cors_methods", when_used='always')
    def encode_cors_methods(self, value: Optional[str]) -> str:
        return value or ''
    
    @field_serializer("cors_headers", when_used='always')
    def encode_cors_headers(self, value: Optional[str]) -> str:
        return value or ''

def get_settings() -> Settings:
    log.info('Getting settings')
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', '.env'))
    log.info(f'Environment file path: {env_path}')
    if os.path.exists(env_path):
        log.info(f'Loading environment variables from {env_path}')
    else:
        log.warning(f'No environment file found at {env_path}')
    
    load_dotenv(dotenv_path=env_path)
    env = os.getenv('ENV', 'local')
    log.info(f'Environment: {env}')
    
    env_file_mapping = {
        'local': '.env.local',
        'dev': '.env.dev',
        'prod': '.env.prod',
    }
    
    env_file_path = env_file_mapping.get(env, '.env.local')
    
    return Settings(_env_file=env_file_path, _env_file_encoding='utf-8')
    
settings = get_settings()
