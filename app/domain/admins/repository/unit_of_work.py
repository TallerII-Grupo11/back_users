import abc
from app.domain.admins.repository.admin_repository import AdminRepository


class AbstractAdminUnitOfWork(abc.ABC):
    repository: AdminRepository

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
