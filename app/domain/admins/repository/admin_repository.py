import abc
from typing import List, Optional

from app.domain.admins.model.admin import Admin
from app.domain.admins.model.admin_id import AdminId


class AdminRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, admin: Admin):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, admin_id: AdminId) -> Admin:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_email(self, email: str) -> Admin:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_firebase_id(self, firebase_id: str) -> Admin:
        raise NotImplementedError

    @abc.abstractmethod
    def all(
        self,
        firebase_id: Optional[str],
        email: Optional[str],
        user_ids: Optional[str],
        offset: int,
        limit: int,
    ) -> List[Admin]:
        raise NotImplementedError

    @abc.abstractmethod
    def total(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, admin: Admin):
        raise NotImplementedError
