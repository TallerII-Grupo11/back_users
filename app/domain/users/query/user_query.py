from typing import Optional

from pydantic.main import BaseModel


class UserQuery(BaseModel):
    firebase_id: Optional[str] = None
    email: Optional[str] = None
    user_ids: Optional[str] = None
    offset: int = 0
    limit: int = 100
