import logging
from typing import List

import uuid as uuid
from app.domain.admins.command.admin_create_command import AdminCreateCommand
from app.domain.admins.command.admin_update_command import AdminUpdateCommand
from app.domain.admins.model.admin import Admin
from app.domain.admins.model.admin_exceptions import (
    AdminAlreadyExistException,
    AdminsNotFoundError,
)
from app.domain.admins.model.admin_id import AdminId
from app.domain.admins.repository.unit_of_work import AbstractAdminUnitOfWork
from app.domain.admins.query.admin_query import AdminQuery


class AdminUseCases:
    def __init__(self, admin_uow: AbstractAdminUnitOfWork):
        self.admin_uow: AbstractAdminUnitOfWork = admin_uow

    def list(self, admin_query: AdminQuery) -> List[Admin]:
        return self.admin_uow.repository.all(
            admin_query.firebase_id,
            admin_query.email,
            admin_query.user_ids,
            admin_query.offset,
            admin_query.limit,
        )

    def register(self, admin_command: AdminCreateCommand) -> Admin:
        try:
            admin = self.admin_uow.repository.find_by_email(admin_command.email)
            if admin:
                raise AdminAlreadyExistException()
            admin_id = AdminId(str(uuid.uuid4()))
            admin = Admin(
                id=admin_id,
                firebase_id=admin_command.firebase_id,
                first_name=admin_command.first_name,
                last_name=admin_command.last_name,
                email=admin_command.email,
            )
            self.admin_uow.repository.save(admin)
            self.admin_uow.commit()
            return self.admin_uow.repository.find_by_id(admin_id)
        except Exception as e:
            logging.error(e)
            self.admin_uow.rollback()
            raise e

    def find_by_id(self, admin_id: str) -> Admin:
        admin = self.admin_uow.repository.find_by_id(AdminId(admin_id))
        if not admin:
            raise AdminsNotFoundError(admin_id)
        return admin

    def update(self, admin_command: AdminUpdateCommand) -> Admin:
        admin = self.find_by_id(admin_command.admin_id)
        if admin is None:
            raise AdminsNotFoundError(admin_command.admin_id)
        try:
            updated_admin = Admin(
                id=AdminId(admin_command.admin_id),
                firebase_id=admin_command.firebase_id,
                first_name=admin_command.first_name,
                last_name=admin_command.last_name,
                email=admin_command.email,
                status=admin_command.status,
            )
            admin.update(updated_admin)
            self.admin_uow.repository.update(admin)
            self.admin_uow.commit()
        except Exception as e:
            logging.error(e)
            self.admin_uow.rollback()
            raise e

        return admin
