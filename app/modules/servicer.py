from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import inspect, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from sqlalchemy.orm import selectinload


# Equivalent to SELECT * FROM table;
async def select_all(session: AsyncSession, table_schema: Base) -> list:
    query = select(table_schema)
    response = await session.execute(query)
    results = response.scalars().all()

    return results


async def select_all_extended(
    session: AsyncSession,
    table_schema: Base,
    attribute_name: str
) -> list:
    attribute = getattr(table_schema, attribute_name, None)

    if attribute is None:
        raise ValueError(
            f"{attribute_name} is not a valid relationship attribute in {table_schema.__name__}"
        )

    query = select(table_schema).options(selectinload(attribute))
    response = await session.execute(query)
    results = response.scalars().all()

    return results


async def select_specific(
        session: AsyncSession,
        table_schema: Base,
        id: UUID
) -> Base:
    result = await session.get(table_schema, id)
    if result is None:
        raise NoResultFound("Record not found")

    return result


async def select_specific_extended(
    session: AsyncSession,
    table_schema: Base,
    id: UUID,
    attribute_name: str
) -> Base:
    table_id = inspect(table_schema).primary_key[0]
    attribute = getattr(table_schema, attribute_name, None)

    if attribute is None:
        raise ValueError(
            f"{attribute_name} is not a valid relationship attribute in {table_schema.__name__}"
        )

    query = select(table_schema).options(selectinload(attribute)).where(table_id == id)
    result = await session.execute(query)

    if result is None:
        raise NoResultFound("Record not found")

    return result.scalars().first()


async def insert_into(session: AsyncSession, table_schema: Base, insert_data: BaseModel) -> Base:
    insert_model = table_schema(
        **insert_data.dict(exclude_none=True, exclude_unset=True)
    )  # pk is auto-generated

    session.add(insert_model)
    await session.commit()
    await session.refresh(insert_model)

    return insert_model


async def update_record(
    session: AsyncSession,
    table_schema: Base,
    id: UUID,
    update_data: BaseModel
) -> Base:
    update_model = await select_specific(session=session, table_schema=table_schema, id=id)

    update_data = update_data.dict(exclude_none=True, exclude_unset=True)

    for key, value in update_data.items():
        if hasattr(update_model, key):
            setattr(update_model, key, value)

    session.add(update_model)
    await session.commit()
    await session.refresh(update_model)

    return update_model


async def delete_record(session: AsyncSession, table_schema: Base, id: UUID) -> None:
    delete_model = await select_specific(session=session, table_schema=table_schema, id=id)
    await session.delete(delete_model)
    await session.commit()
