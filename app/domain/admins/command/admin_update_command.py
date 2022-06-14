from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel

from app.domain.admins.model.admin import AdminStatus


class AdminUpdateCommand(BaseModel):
    admin_id: str
    firebase_id: str
    first_name: str
    last_name: str
    status: Optional[AdminStatus] = AdminStatus.ACTIVE
    email: EmailStr
