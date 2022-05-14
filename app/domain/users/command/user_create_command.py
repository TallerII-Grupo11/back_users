from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel

from app.domain.users.model.user import UserRole


class UserCreateCommand(BaseModel):
    firebase_id: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.LISTENER
    email: EmailStr
    # password: str
    location: Optional[str] = None
