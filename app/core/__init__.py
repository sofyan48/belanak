from pydantic_settings import BaseSettings
from enum import Enum
import os

class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    PROJECT_NAME: str = "app"
    MODE: ModeEnum = ModeEnum.development
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/ex/{API_VERSION}"

    class Config:
        case_sensitive = True


settings = Settings()