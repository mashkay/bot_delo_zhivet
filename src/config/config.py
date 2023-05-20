import logging
from enum import Enum

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Base(BaseSettings):
    app_title: str = "Сервис Дело Живет"
    AM_I_IN_A_DOCKER_CONTAINER:bool = False


    class PostgresLocal:
        POSTGRES_USER: str 
        POSTGRES_PASSWORD: str
        DB_HOST: str
        DB_PORT: str
        POSTGRES_DB: str
    
    class PostgresContainer(BaseSettings):
        POSTGRES_USER: str
        POSTGRES_PASSWORD: str
        DB_HOST: str
        DB_PORT: str
        POSTGRES_DB: str
    

    # Postgres/Postgis
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str

    # Telegram
    TELEGRAM_BOT_TOKEN: str = None
    WEBHOOK_DOMAIN: str = None
    WEBHOOK_PORT: int = None
    WEBHOOK_PATH: str = None
    HOST: str = None

    # AWS (YANDEX OBJECT STORAGE)
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SERVICE_NAME: str
    AWS_ENDPOINT_URL: str
    AWS_BUCKET_NAME: str

    # SENTRY
    SENTRY_DSN_BOT: str = None
    SENTRY_DSN_ADMIN: str | None = None

    # Celery
    redis_host: str | None = "redis"
    redis_port: str | None = "6379"
    celery_connect_string = "redis://{}:{}/0"

    # Logging
    logger_name: str = "bot"
    log_file: str | None = "bot.log"
    log_level: int | None = logging.INFO
    log_encoding: str | None = "utf-8"

    # flask
    ADMIN_SECRET_KEY: str = "SECRET_KEY"
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:" f"{POSTGRES_PASSWORD}@" f"{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    FLASK_ENV: str = "development"

    # First superuser
    SUPER_USER_LOGIN: str
    SUPER_USER_EMAIL: str
    SUPER_USER_PASSWORD: str

    # Дополнительные параметры, не участвующие в ините приложения
    BOOTSTRAP_VERSION = "bootstrap4"
    LOG_DEFAULT_LVL = logging.DEBUG
    LOG_EXTENSION = ".log"
    LOG_FORMAT = "%(asctime)s [%(levelname)s]  %(message)s"
    LOG_REL_PATH = "logs"

    # Параметры почтового клиента
    MAIL_SERVER: str = "smtp.yandex.ru"
    MAIL_PORT: int = 465
    MAIL_USE_SSL: bool = True
    MAIL_USERNAME: str = "test.delo.zhivet@yandex.ru"
    MAIL_PASSWORD: str = "bctlgfnckbtxhgzt"
    MAIL_DEBUG: int = 1

    # Параметры генерации токенов сброса пароля
    PASSWORD_RESET_TOKEN_TTL: int = 600
    PASSWORD_RESET_TOKEN_ALGORITHM: str = "HS256"

    # YANDEX TRACKER
    OAUTH_TOKEN: str
    ORG_ID: int

    # GEOCODER API
    GEOCODER_APIKEY: str | None = None
    GEOCODER_BASE_URL: str = "https://geocode-maps.yandex.ru/1.x/"
    MAXIMUM_OBJECTS_FROM_GEOCODER: int = 10

    # DADATA
    DADATA_TOKEN: str
    DADATA_SECRET: str

    @property
    def postgres(self):
        if self.AM_I_IN_A_DOCKER_CONTAINER:
            return self.PostgresContainer
        return self.PostgresLocal


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DevConfig(Base):
    pass


class ProdConfig(Base):
    pass


settings = Base()
print(settings)