from fastapi import status, Request

from starlette.responses import JSONResponse

from app.domain.users.model.user_exceptions import (
    UserAlreadyExistException,
    UserAlreadyHadStatusError,
    UserAlreadyHadRoleError,
    UsersNotFoundError,
    InvalidCredentialsError,
    UsersBlockedException,
)


async def user_already_exist_exception_handler(
    request: Request, exc: UserAlreadyExistException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=exc.message,
    )


async def user_already_had_status_exception_handler(
    request: Request, exc: UserAlreadyHadStatusError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=exc.message,
    )


async def user_already_had_role_exception_handler(
    request: Request, exc: UserAlreadyHadRoleError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=exc.message,
    )


async def user_not_found_exception_handler(
    request: Request, exc: UsersNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.message,
    )


async def wrong_credentials_exception_handler(
    request: Request, exc: InvalidCredentialsError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=exc.message,
    )


async def user_blocked_exception_handler(
    request: Request, exc: UsersBlockedException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=exc.message,
    )
