from fastapi import status, Request

from starlette.responses import JSONResponse

from app.domain.admins.model.admin_exceptions import (
    AdminAlreadyExistException,
    AdminsNotFoundError,
    AdminsBlockedException,
)


async def admin_already_exist_exception_handler(
    request: Request, exc: AdminAlreadyExistException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.message,
    )


async def admin_not_found_exception_handler(
    request: Request, exc: AdminsNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.message,
    )


async def admin_blocked_exception_handler(
    request: Request, exc: AdminsBlockedException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=exc.message,
    )
