"""
Application configuration management.
Loads environment variables and provides settings throughout the application.
"""
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, EmailStr, field_validator, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


def parse_cors_origins(v: Union[str, List[str]]) -> List[str]:
    """Parse CORS origins from comma-separated string or list."""
    if isinstance(v, str) and v:
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list):
        return v
    return []


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    # Application
    APP_NAME: str = "SwimUSA Recruit API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    API_V1_PREFIX: str = "/api/v1"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str
    DATABASE_SYNC_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Email Configuration
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: EmailStr = "noreply@swimusarecruit.com"
    MAIL_FROM_NAME: str = "SwimUSA Recruit"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    MAIL_USE_CREDENTIALS: bool = False

    # AWS S3
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: Optional[str] = None
    S3_BUCKET_URL: Optional[str] = None

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Celery
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None

    # Frontend
    FRONTEND_URL: str

    # CORS
    CORS_ORIGINS: Annotated[List[str], BeforeValidator(parse_cors_origins)] = []

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "doc", "docx", "jpg", "jpeg", "png", "mp4", "mov"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # NCAA
    NCAA_STANDARDS_URL: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # Admin User
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    ADMIN_FIRST_NAME: str = "Admin"
    ADMIN_LAST_NAME: str = "User"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields like SUPABASE_URL (used by frontend only)
        env_parse_none_str="null",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """Customize settings sources to handle CORS_ORIGINS properly."""
        from pydantic_settings import DotEnvSettingsSource

        class CustomDotEnvSettingsSource(DotEnvSettingsSource):
            def prepare_field_value(self, field_name, field, value, value_is_complex):
                # Don't try to JSON parse CORS_ORIGINS, let the validator handle it
                if field_name == "CORS_ORIGINS":
                    return value
                return super().prepare_field_value(field_name, field, value, value_is_complex)

        return (
            init_settings,
            env_settings,
            CustomDotEnvSettingsSource(
                settings_cls,
                env_file=cls.model_config.get('env_file'),
                env_file_encoding=cls.model_config.get('env_file_encoding'),
                case_sensitive=cls.model_config.get('case_sensitive'),
            ),
            file_secret_settings,
        )

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"


# Create a global settings instance
settings = Settings()
