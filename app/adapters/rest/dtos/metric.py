from pydantic.main import BaseModel


class MetricRequestDto(BaseModel):
    id: str


class MetricResponseDto(BaseModel):
    id: str
    name: str
