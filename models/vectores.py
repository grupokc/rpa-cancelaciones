from models import * 
from pydantic import BaseModel, Field 


class Point(BaseModel):
    x: int
    y: int

class Regions(BaseModel): 
    left: int 
    top: int 
    width: int
    height: int 

class UIMap(BaseModel):
    version: int
    profile: str
    points: dict[str, Point] = Field(default_factory=dict)
    regions: dict[str, Regions] = Field(default_factory=dict)