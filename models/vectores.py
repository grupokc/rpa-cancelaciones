from models import * 
from pydantic import BaseModel, Field 

class Point(BaseModel):
    x: int
    y: int


class UIMap(BaseModel):
    version: int
    profile: str
    points: dict[str, Point] = Field(default_factory=dict)
