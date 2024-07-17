from pydantic import BaseModel


class CityHistorySchema(BaseModel):
    city: str
    count: int
