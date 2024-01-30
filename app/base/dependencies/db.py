from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import session_factory, SessionFactoryType


async def get_session() -> AsyncGenerator[AsyncSession, SessionFactoryType]:
    async with session_factory() as db_session:
        yield db_session