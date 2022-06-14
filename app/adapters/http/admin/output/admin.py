from typing import Optional

from pydantic import EmailStr, validator
from pydantic.main import BaseModel


class AdminId(BaseModel):
    id: str

    class Config:
        orm_mode = True


class AdminResponse(BaseModel):
    id: AdminId
    firebase_id: str
    email: EmailStr
    first_name: str
    last_name: str
    status: Optional[str]

    @validator('id')
    def map_id(cls, v):
        return v.id

    class Config:
        orm_mode = True
