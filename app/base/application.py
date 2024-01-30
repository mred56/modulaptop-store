from fastapi import APIRouter, FastAPI
from .settings import settings
import logging
import httpx

from app.modules.healthcheck.view import router as healthcheck_router
from app.modules.customers.view import router as customers_router
from app.modules.shipments.view import router as shipments_router
from app.modules.orders.view import router as orders_router
from app.modules.laptops.view import router as laptop_router
from app.modules.components.view import router as components_router


logger = logging.getLogger(__name__)


def setup_routing(app_instance: FastAPI):
    global_router = APIRouter()
    global_router.include_router(healthcheck_router, tags=["healthcheck"])
    global_router.include_router(customers_router, tags=["customers"])
    global_router.include_router(shipments_router, tags=["shipments"])
    global_router.include_router(orders_router, tags=["orders"])
    global_router.include_router(laptop_router, tags=["laptops"])
    global_router.include_router(components_router, tags=["components"])

    app_instance.include_router(global_router)


def setup_httpx_client(app_instance: FastAPI) -> FastAPI:
    transport = httpx.AsyncHTTPTransport(retries=2)
    app_instance.state.http_client = httpx.AsyncClient(
        transport=transport,
        timeout=settings.HTTP_CLIENT_TIMEOUT.total_seconds(),
    )
    app_instance.add_event_handler(
        "shutdown",
        app_instance.state.http_client.aclose,
    )
    return app_instance


def create_app() -> FastAPI:
    app_instance = FastAPI(
        title="Precious",
        version=settings.VERSION,
        docs_url="/redoc",
        root_path=settings.APP_ROOT_PATH,
    )
    setup_routing(app_instance)
    setup_httpx_client(app_instance)

    return app_instance
