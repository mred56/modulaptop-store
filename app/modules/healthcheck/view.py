from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.base.dependencies.db import get_session

router = APIRouter()


@router.get("/api/healthcheck", tags=["healthcheck"])
async def healthcheck(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    is_database_working = True
    output = "ok"

    try:
        db_response = await session.execute(text("SELECT 1"))
        db_response.fetchone()
    except Exception as e:
        output = str(e)
        is_database_working = False

    return {
        "is_database_working": is_database_working,
        "output": output,
        "version": request.app.version,
    }
