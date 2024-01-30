import uvicorn
import app.base.application as application
from app.base.settings import settings


app = application.create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # noqa
        port=settings.APPLICATION_PORT,
        reload=settings.DEBUG,
        log_config=None,
    )
