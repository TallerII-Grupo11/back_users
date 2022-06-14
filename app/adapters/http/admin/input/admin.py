from pydantic import EmailStr, Field
from pydantic.main import BaseModel
from typing import Optional

from app.domain.admins.command.admin_update_command import AdminUpdateCommand
from app.domain.admins.model.admin import AdminStatus

from app.domain.admins.command.admin_create_command import AdminCreateCommand


class AdminRequest(BaseModel):
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    first_name: str = Field(example="Juan")
    last_name: str = Field(example="Perez")
    email: EmailStr = Field(example="username@mail.com")

    def to_create_admin_command(self):
        return AdminCreateCommand(
            email=self.email,
            firebase_id=self.firebase_id,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class AdminUpdateRequest(AdminRequest):
    status: Optional[AdminStatus] = Field(example=AdminStatus.ACTIVE)

    def to_update_admin_command(self, admin_id: str):
        return AdminUpdateCommand(
            admin_id=admin_id,
            email=self.email,
            firebase_id=self.firebase_id,
            first_name=self.first_name,
            last_name=self.last_name,
            status=self.status,
        )
