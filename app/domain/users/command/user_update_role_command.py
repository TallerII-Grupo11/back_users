from pydantic import BaseModel


class UpdateUserRoleCommand(BaseModel):
    user_id: str
    role: str
