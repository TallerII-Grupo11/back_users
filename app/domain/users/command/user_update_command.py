from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel

from app.domain.users.model.user import UserStatus, UserRole


class UserUpdateCommand(BaseModel):
    user_id: str
    firebase_id: str
    first_name: str
    last_name: str
    role: Optional[UserRole] = UserRole.LISTENER
    status: Optional[UserStatus] = UserStatus.ACTIVE
    email: EmailStr
    # password: str
    location: Optional[str] = None
