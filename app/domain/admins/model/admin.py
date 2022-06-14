from typing import Optional, Union

from enum import Enum
from pydantic import BaseModel, Field
from pydantic.schema import date

from app.domain.admins.model.admin_id import AdminId


class AdminStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BLOCKED = 'BLOCKED'


class Admin(BaseModel):
    id: AdminId = Field(example="123e4567-e89b-12d3-a456-426614174000")
    firebase_id: str = Field(example="abc123fg-e14j-19jf-12fo-412319014050")
    email: str = Field(example="juanperez@mail.com")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    status: Optional[AdminStatus] = Field(
        AdminStatus.ACTIVE, example=AdminStatus.ACTIVE
    )
    created_at: Union[str, date, None] = Field(example="Created")
    updated_at: Union[str, date, None] = Field(example="Updated")

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def update(self, user: "Admin"):
        self.status = user.status
        self.firebase_id = user.firebase_id
        self.email = user.email
        self.first_name = user.first_name
        self.last_name = user.last_name

    def is_blocked(self):
        return AdminStatus.BLOCKED == self.status
