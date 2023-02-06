import asyncio
from logging.config import fileConfig

from alembic import context
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine

from app.core.config import settings
from app.db.models import DefaultBase

config = context.config
config.set_main_option("sqlalchemy.url", settings.POSTGRES_URL)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = DefaultBase.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""

    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    connectable = AsyncEngine(
        create_engine(
            config.get_main_option("sqlalchemy.url"),
            echo=True,
            future=True,
        ),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
