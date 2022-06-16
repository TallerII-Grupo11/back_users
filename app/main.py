import uvicorn


from app.adapters.http.health import health_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
import logging.config

from app.adapters.http.users import users_controller
from app.adapters.http.users.exceptions_handler import (
    user_already_exist_exception_handler,
    user_already_had_status_exception_handler,
    user_already_had_role_exception_handler,
    user_not_found_exception_handler,
    user_blocked_exception_handler,
    wrong_credentials_exception_handler,
)

from app.domain.users.model.user_exceptions import (
    UserAlreadyExistException,
    UserAlreadyHadStatusError,
    UserAlreadyHadRoleError,
    UsersNotFoundError,
    InvalidCredentialsError,
    UsersBlockedException,
)

from app.adapters.http.admin import admin_controller
from app.adapters.http.admin.exceptions_handler import (
    admin_already_exist_exception_handler,
    admin_not_found_exception_handler,
    admin_blocked_exception_handler,
)

from app.domain.admins.model.admin_exceptions import (
    AdminAlreadyExistException,
    AdminsNotFoundError,
    AdminsBlockedException,
)

from app.conf.config import Settings

logging.config.fileConfig('app/conf/logging.conf', disable_existing_loggers=False)

settings = Settings()

app = FastAPI(
    version=settings.version, title=settings.title, description=settings.description
)

app.add_middleware(DBSessionMiddleware, db_url=settings.database_url)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup():
    logger.info("Startup APP")


@app.on_event("shutdown")
async def shutdown():
    logger.info("Shutdown APP")


app.include_router(admin_controller.router)
app.include_router(users_controller.router)
app.include_router(health_controller.router)

app.add_exception_handler(
    UserAlreadyExistException, user_already_exist_exception_handler
)
app.add_exception_handler(
    UserAlreadyHadStatusError, user_already_had_status_exception_handler
)
app.add_exception_handler(
    UserAlreadyHadRoleError, user_already_had_role_exception_handler
)
app.add_exception_handler(UsersNotFoundError, user_not_found_exception_handler)
app.add_exception_handler(InvalidCredentialsError, wrong_credentials_exception_handler)

app.add_exception_handler(UsersBlockedException, user_blocked_exception_handler)

app.add_exception_handler(
    AdminAlreadyExistException, admin_already_exist_exception_handler
)
app.add_exception_handler(AdminsNotFoundError, admin_not_found_exception_handler)

app.add_exception_handler(AdminsBlockedException, admin_blocked_exception_handler)


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=settings.port)
