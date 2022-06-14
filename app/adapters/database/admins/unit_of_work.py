from sqlalchemy.orm import Session

from app.domain.admins.repository.unit_of_work import AbstractAdminUnitOfWork
from app.domain.admins.repository.admin_repository import AdminRepository


class AdminUnitOfWork(AbstractAdminUnitOfWork):
    def __init__(self, repository: AdminRepository, session: Session):
        self.session = session
        self.repository = repository

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
