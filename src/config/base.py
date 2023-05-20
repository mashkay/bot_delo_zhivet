from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class BaseConfig(BaseSettings):
    app_title: str = "Сервис Дело Живет"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str
    TELEGRAM_BOT_TOKEN: str = None
    WEBHOOK_DOMAIN: str = None
    WEBHOOK_PORT: int = None
    WEBHOOK_PATH: str = None
    HOST: str = None
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SERVICE_NAME: str
    AWS_ENDPOINT_URL: str
    AWS_BUCKET_NAME: str
    SENTRY_DSN_BOT: str = None

    # Celery
    redis_host: str | None = "redis"
    redis_port: str | None = "6379"
    celery_connect_string = "redis://{}:{}/0"

    # Logging
    logger_name: str = "bot"
    log_file: str | None = "bot.log"
    log_level: int | None = INFO
    log_encoding: str | None = "utf-8"


    SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", default="SECRET_KEY")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = "development"

    SENTRY_DSN_ADMIN = os.getenv("SENTRY_DSN_ADMIN", default=None)

    # Дополнительные параметры, не участвующие в ините приложения
    BOOTSTRAP_VERSION = "bootstrap4"
    LOG_DEFAULT_LVL = logging.DEBUG
    LOG_EXTENSION = ".log"
    LOG_FORMAT = "%(asctime)s [%(levelname)s]  %(message)s"
    LOG_REL_PATH = "logs"

    # Параметры почтового клиента
    MAIL_SERVER = os.getenv("MAIL_SERVER", default="smtp.yandex.ru")
    MAIL_PORT = os.getenv("MAIL_PORT", default=465)
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", default=True)
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", default="test.delo.zhivet@yandex.ru")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", default="bctlgfnckbtxhgzt")
    MAIL_DEBUG = os.getenv("MAIL_DEBUG", default=1)

    # Параметры генерации токенов сброса пароля
    PASSWORD_RESET_TOKEN_TTL = 600
    PASSWORD_RESET_TOKEN_ALGORITHM = os.getenv("PASSWORD_RESET_TOKEN_ALGORITHM", default="HS256")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = BaseSettings()