import abc
from typing import List, Optional

from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId


class UserRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_id(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def all(
        self, firebase_id: Optional[str], email: Optional[str], offset: int, limit: int
    ) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def total(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, user: User):
        raise NotImplementedError
