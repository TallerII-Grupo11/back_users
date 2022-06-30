from pydantic.fields import Field
from pydantic.main import BaseModel


class LoginRequest(BaseModel):
    federated: bool = Field(example=False, default=False)
