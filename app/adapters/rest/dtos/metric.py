from pydantic.main import BaseModel


class MetricResponseDto(BaseModel):
    id: str
    name: str
