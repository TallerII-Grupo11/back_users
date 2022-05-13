import logging
from typing import List

import uuid as uuid
from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.command.user_update_role_command import UpdateUserRoleCommand
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.model.user import User, UserStatus, UserRole
from app.domain.users.model.user_exceptions import (
    UserAlreadyExistException,
    UsersNotFoundError,
)
from app.domain.users.model.user_id import UserId
from app.domain.users.repository.unit_of_work import AbstractUserUnitOfWork
from app.domain.users.query.user_query import UserQuery


class UserUseCases:
    def __init__(self, user_uow: AbstractUserUnitOfWork):
        self.user_uow: AbstractUserUnitOfWork = user_uow

    def list(self, user_query: UserQuery) -> List[User]:
        return self.user_uow.repository.all(
            user_query.q, user_query.offset, user_query.limit
        )

    def register(self, user_command: UserCreateCommand) -> User:
        try:
            user = self.user_uow.repository.find_by_email(user_command.email)
            if user:
                raise UserAlreadyExistException()
            user_id = UserId(str(uuid.uuid4()))
            # user_id = UserId(user_command.firebase_id)
            user = User(
                id=user_id,
                firebase_id=user_command.firebase_id,
                first_name=user_command.first_name,
                last_name=user_command.last_name,
                email=user_command.email,
                location=user_command.location,
                role=user_command.role,
            )
            self.user_uow.repository.save(user)
            self.user_uow.commit()
            return self.user_uow.repository.find_by_id(user_id)
        except Exception as e:
            logging.error(e)
            self.user_uow.rollback()
            raise e

    def find_by_id(self, user_id: str) -> User:
        user = self.user_uow.repository.find_by_id(UserId(user_id))
        if not user:
            raise UsersNotFoundError(user_id)
        return user

    def update_status(
        self, update_user_status_command: UpdateUserStatusCommand
    ) -> User:
        user = self.user_uow.repository.find_by_id(
            UserId(update_user_status_command.user_id)
        )
        if user is None:
            raise UsersNotFoundError(update_user_status_command.user_id)
        try:
            user.update_status(UserStatus(update_user_status_command.status))
            self.user_uow.repository.update(user)
            self.user_uow.commit()
        except Exception as e:
            logging.error(e)
            self.user_uow.rollback()
            raise e

        return user

    def update_role(self, update_user_role_command: UpdateUserRoleCommand) -> User:
        user = self.user_uow.repository.find_by_id(
            UserId(update_user_role_command.user_id)
        )
        if user is None:
            raise UsersNotFoundError(update_user_role_command.user_id)
        try:
            user.update_role(UserRole(update_user_role_command.role))
            self.user_uow.repository.update(user)
            self.user_uow.commit()
        except Exception as e:
            logging.error(e)
            self.user_uow.rollback()
            raise e

        return user
