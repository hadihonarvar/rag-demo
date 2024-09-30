import os
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Literal
from dotenv import load_dotenv
from app.utils.logger import log

EnvType = Literal['local', 'dev', 'prod']

class Settings(BaseSettings):
    app_name: str = 'Demo Store'
    author: str = 'Mamamd Agha'
    environment: str = 'local'

    ENV: Optional[str] = 'local'

    FASTAPI_HOST: str = ''
    FASTAPI_PORT: str = '9000'

    cors_origins: List[str] = ['*']
    cors_methods: List[str] = ['*']
    cors_headers: List[str] = ['*']

    DB_PSQL_NAME: str = 'postgres'
    DB_PSQL_HOST: str = 'localhost'
    DB_PSQL_PORT: str = '5432'
    DB_PSQL_USER: str = 'postgres'
    DB_PSQL_PASSWORD: str = 'password'

    DB_QDRANT_NAME: str = 'qdrant'
    DB_QDRANT_HOST: str = 'localhost'
    DB_QDRANT_PORT: str = '6333'
    DB_QDRANT_USER: str = 'admin'
    DB_QDRANT_PASSWORD: str = 'password'

    OPENAI_API_KEY: str = ''

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @validator("cors_origins", "cors_methods", "cors_headers", pre=True, each_item=True)
    def encode_list(cls, v):
        if isinstance(v, list):
            return ','.join(element if ',' not in element else f'"{element}"' for element in v)
        return v

    @validator("FASTAPI_HOST", "FASTAPI_PORT", "DB_PSQL_NAME", "DB_QDRANT_NAME", pre=True)
    def encode_optional_str(cls, v):
        return v or ''

def get_settings() -> Settings:
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', '.env'))

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
