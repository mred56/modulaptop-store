import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, text, delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from pydantic import PostgresDsn
from app.db.models.component_order import ComponentOrderTable
from app.db.models.components import ComponentsTable

from app.db.models.customers import CustomersTable

from app.base.settings import settings
from app.base.constants import PROJECT_ROOT_PATH
from app.db.models.laptop_order import LaptopOrderTable
from app.db.models.laptops import LaptopsTable
from app.db.models.laptops_components import LaptopsComponentsTable
from app.db.models.orders import OrdersTable
from app.db.models.shipments import ShipmentsTable
from app.db.session import ASYNC_URI
from tests.factories import inject_session


test_engine = create_async_engine(
    ASYNC_URI,
    echo=settings.DEBUG,
    connect_args={"server_settings": {"application_name": settings.POSTGRES_APPLICATION_NAME}},
    poolclass=StaticPool,
)
async_session = async_sessionmaker(
    test_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def clear_database_data():
    async with async_session() as session:
        await session.execute(delete(CustomersTable))
        await session.execute(delete(ShipmentsTable))
        await session.execute(delete(LaptopsTable))
        await session.execute(delete(ComponentsTable))
        await session.execute(delete(OrdersTable))
        await session.execute(delete(LaptopOrderTable))
        await session.execute(delete(ComponentOrderTable))
        await session.execute(delete(LaptopsComponentsTable))
        await session.commit()


def create_test_database_if_not_exists(alembic_engine: Engine):
    # make sure that connection is off
    asyncio.get_event_loop().run_until_complete(test_engine.dispose())
    alembic_engine.dispose()
    engine = create_engine(
        PostgresDsn.build(
            scheme="postgresql",
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            path=f"/postgres",
        ),
        isolation_level="AUTOCOMMIT",
    )
    with engine.connect() as con:
        con.execute(text(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB} WITH (FORCE)"))
        con.execute(text(f"CREATE DATABASE {settings.POSTGRES_DB}"))


@pytest.fixture(scope="session", autouse=True)
def db_init(alembic_engine, alembic_config):
    engine = alembic_engine
    alembic_upgrade(alembic_config, "head")
    connection = engine.connect()
    yield connection
    connection.close()


@pytest_asyncio.fixture
async def db_cleanup(db_init):
    await clear_database_data()
    yield


@pytest.fixture(scope="session")
def alembic_engine() -> Engine:
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    create_test_database_if_not_exists(engine)
    return engine


@pytest.fixture(scope="session")
def alembic_config() -> AlembicConfig:
    alembic_config = AlembicConfig(str(PROJECT_ROOT_PATH / "alembic.ini"))
    alembic_config.set_main_option(
        "script_location",
        str(PROJECT_ROOT_PATH / alembic_config.get_main_option("script_location")),
    )
    alembic_config.set_main_option(
        "sqlalchemy.url",
        settings.SQLALCHEMY_DATABASE_URI,
    )
    return alembic_config


@pytest_asyncio.fixture
async def db_session(init_app, db_init, db_cleanup):
    async with async_session() as session:
        inject_session(session)
        yield session

