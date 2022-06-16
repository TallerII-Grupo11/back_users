from pydantic import EmailStr
from pydantic.main import BaseModel


class AdminCreateCommand(BaseModel):
    firebase_id: str
    first_name: str
    last_name: str
    email: EmailStr
