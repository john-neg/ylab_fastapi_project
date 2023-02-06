import os

from dotenv import load_dotenv
from openpyxl.styles import Alignment, Border, Font, NamedStyle, PatternFill, Side
from pydantic.env_settings import BaseSettings
from pydantic.networks import AmqpDsn, AnyHttpUrl, PostgresDsn, RedisDsn

BASEDIR: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
)
load_dotenv(os.path.join(BASEDIR, ".env"))


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = os.getenv("SERVER_NAME", default="localhost")
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    FILES_DIR: str = os.path.join(BASEDIR, "files")

    # PostgreSQL database settings
    PG_DB_NAME: str = os.getenv("DB_NAME", default="postgres")
    PG_USER: str = os.getenv("POSTGRES_USER", default="postgres")
    PG_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", default="postgres")
    PG_DB_HOST: str = os.getenv("DB_HOST", default="localhost")
    PG_DB_PORT: str = os.getenv("DB_PORT", default="5432")
    POSTGRES_URL: str = PostgresDsn.build(
        scheme="postgresql+asyncpg",
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_DB_HOST,
        port=PG_DB_PORT,
        path=f"/{PG_DB_NAME}",
    )

    # Redis settings
    REDIS_HOST: str = os.getenv("REDIS_HOST", default="localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", default="6379")
    REDIS_CACHE_TIME: str | int = os.getenv("REDIS_CACHE_TIME", default=3600)
    REDIS_URL: str = RedisDsn.build(
        scheme="redis",
        host=REDIS_HOST,
        port=REDIS_PORT,
    )

    # RabbitMQ settings
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", default="localhost")
    RABBITMQ_PORT: str = os.getenv("RABBITMQ_PORT", default="5672")
    RABBITMQ_DEFAULT_USER: str = os.getenv(
        "RABBITMQ_DEFAULT_USER",
        default="rabbit",
    )
    RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBIT_PASSWORD", default="rabbit")

    # Celery settings
    CELERY_BROKER_URL: str = AmqpDsn.build(
        scheme="amqp",
        user=RABBITMQ_DEFAULT_USER,
        password=RABBITMQ_DEFAULT_PASS,
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
    )
    CELERY_BACKEND_URL: str = "rpc://"


class ExcelStyle:
    """Styles for Excel file report."""

    FileType = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    ThinBorder = Side(style="thin", color="000000")
    ThickBorder = Side(style="thick", color="000000")
    AllBorder = Border(
        left=ThinBorder, right=ThinBorder, top=ThinBorder, bottom=ThinBorder
    )
    GreyFill = PatternFill(
        start_color="CCCCCC",
        end_color="CCCCCC",
        fill_type="solid",
    )

    Header = NamedStyle(name="header")
    Header.font = Font(size=12, bold=True)
    Header.border = AllBorder
    Header.alignment = Alignment(wrap_text=True)

    BaseBold = NamedStyle(name="base_bold")
    BaseBold.font = Font(size=11, bold=True)
    BaseBold.border = AllBorder
    BaseBold.alignment = Alignment(wrap_text=True)

    Base = NamedStyle(name="base")
    Base.font = Font(size=11)
    Base.border = AllBorder
    Base.alignment = Alignment(wrap_text=True)


settings = Settings()
