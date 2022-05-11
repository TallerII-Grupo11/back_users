from functools import lru_cache
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.adapters.database.database import get_session_factory
from app.adapters.database.users.sql_user_repository import SQLUserRepository
from app.adapters.database.users.unit_of_work import UserUnitOfWork
from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork
from app.domain.users.repository.user_repository import UserRepository
from app.conf.config import Settings
from app.domain.users.usecases.user import UserUseCases


@lru_cache()
def get_settings():
    return Settings()


def get_session(settings: Settings = Depends(get_settings)) -> Iterator[Session]:
    SessionFactory: Session = get_session_factory(settings)
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


def user_repository_dependency(
        session: Session = Depends(get_session),
) -> UserRepository:
    return SQLUserRepository(session)


def user_uow_dependency(
        session: Session = Depends(get_session),
        user_repository: UserRepository = Depends(user_repository_dependency),
) -> AbstractUserUnitOfWork:
    return UserUnitOfWork(user_repository, session)


def user_usecases_dependency(
        user_uow: AbstractUserUnitOfWork = Depends(user_uow_dependency),
) -> UserUseCases:
    return UserUseCases(user_uow)
