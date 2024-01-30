import logging
import typing as t
import asyncpg
from contextlib import asynccontextmanager
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound, DBAPIError

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from app.base.settings import settings


assert settings.SQLALCHEMY_DATABASE_URI
ASYNC_URI: str = settings.SQLALCHEMY_DATABASE_URI.replace(
    "postgresql",
    "postgresql+asyncpg",
    1,
)

engine = create_async_engine(
    ASYNC_URI,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    pool_timeout=120,
    connect_args={"server_settings": {"application_name": settings.POSTGRES_APPLICATION_NAME}},
)
async_session = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def _can_commit_transaction_with_exception(exc: Exception) -> bool:
    if status_code := getattr(exc, "status_code", None):
        return t.cast(bool, 200 <= status_code < 400)
    return False


@asynccontextmanager
async def session_factory() -> t.AsyncGenerator[AsyncSession, None]:
    """
    All endpoints should be wrapped into session_factory context manager.
    Knows transaction issues in fastAPI:
        * https://github.com/tiangolo/fastapi/issues/2142
        * https://github.com/tiangolo/fastapi/issues/2662

    Others workarounds for transaction with
        `yield Dependency Injection` & `Middleware not working` with
        custom exception handlers [https://fastapi.tiangolo.com/tutorial/handling-errors/].

    Third workaround, `session_decorator`, is less explicit than `context manager`.
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as exc:
            if not _can_commit_transaction_with_exception(exc):
                await session.rollback()

            logger = logging.getLogger(__name__)

            if isinstance(exc, NoResultFound):
                logger.error(f"NoResultFound: {exc}")
                raise HTTPException(status_code=404, detail=str(exc))
            else:
                logger.error(f"An error occured: {exc}")
            raise
        finally:
            await session.commit()
            await session.close()


SessionFactoryType: t.TypeAlias = t.Callable[..., t.AsyncContextManager[AsyncSession]]
