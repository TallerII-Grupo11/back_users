import uvicorn


from app.adapters.http.health import health_controller
from fastapi import FastAPI
import logging.config

from app.conf.config import Settings

logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)

settings = Settings()

app = FastAPI(
    version=settings.version, title=settings.title, description=settings.description
)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Startup APP")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


app.include_router(health_controller.router)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=settings.port)
