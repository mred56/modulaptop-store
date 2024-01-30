from tests.fixtures import *  # noqa
import pytest
import pytest_asyncio

from fastapi import FastAPI
from collections.abc import Iterator
from httpx import AsyncClient
import asyncio
from asgi_lifespan import LifespanManager
import app.base.application as application


@pytest.fixture(scope="session")
def event_loop():
    event_loop = asyncio.get_event_loop()
    yield event_loop
    event_loop.close()


@pytest_asyncio.fixture(scope="session")
async def init_app() -> Iterator[FastAPI]:
    app = application.create_app()

    async with LifespanManager(app):
        yield app


@pytest_asyncio.fixture(scope="session")
async def app_client(init_app):
    async with AsyncClient(
        app=init_app,
        base_url="http://test",
    ) as client:
        yield client
