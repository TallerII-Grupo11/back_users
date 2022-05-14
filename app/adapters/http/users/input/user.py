from pydantic import EmailStr, Field, validator
from pydantic.main import BaseModel
from typing import Optional
from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.model.user import UserStatus, UserRole


class UserRequest(BaseModel):
    firebase_id: str = Field(example="123e4567-e89b-12d3-a456-426614174000")
    first_name: str = Field(example="Juan")
    # password: str = Field(example="secure")
    last_name: str = Field(example="Perez")
    role: Optional[UserRole] = Field(example="LISTENER")
    location: Optional[str] = Field(example="Buenos Aires, Argentina")
    email: EmailStr = Field(example="username@mail.com")

    def to_create_user_command(self):
        return UserCreateCommand(
            email=self.email,
            firebase_id=self.firebase_id,
            role=self.role,
            # password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            location=self.location,
        )


class UserStatusRequest(BaseModel):
    status: UserStatus


class UserRoleRequest(BaseModel):
    role: UserRole
