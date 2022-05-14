from typing import Optional, Union

from enum import Enum
from pydantic import BaseModel, Field
from pydantic.schema import date

from app.domain.users.model.user_exceptions import (
    UserAlreadyHadStatusError,
    UserAlreadyHadRoleError,
)
from app.domain.users.model.user_id import UserId


class UserStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'


class UserRole(str, Enum):
    LISTENER = 'LISTENER'
    ARTIST = 'ARTIST'


class User(BaseModel):
    id: UserId = Field(example="123e4567-e89b-12d3-a456-426614174000")
    firebase_id: str = Field(example="abc123fg-e14j-19jf-12fo-412319014050")
    email: str = Field(example="juanperez@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    location: Optional[str] = Field(example="Buenos Aires, Argentina")
    status: Optional[UserStatus] = Field(UserStatus.ACTIVE, example=UserStatus.ACTIVE)
    role: Optional[UserRole] = Field(UserRole.LISTENER, example=UserRole.LISTENER)
    created_at: Union[str, date, None] = Field(example="Created")
    updated_at: Union[str, date, None] = Field(example="Updated")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def update(self, user: "User"):
        self.update_status(user.status)
        self.update_role(user.role)
        self.firebase_id = user.firebase_id
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.location = user.location

    def update_status(self, status: UserStatus):
        if self.status == status:
            raise UserAlreadyHadStatusError()
        self.status = status

    def update_role(self, role: UserRole):
        if self.role == role:
            raise UserAlreadyHadRoleError()
        self.role = role

    def is_blocked(self):
        return UserStatus.BLOCKED == self.status

    def is_artist(self):
        return UserRole.ARTIST == self.role
