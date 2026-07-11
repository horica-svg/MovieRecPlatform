from pydantic import BaseModel
from typing import Optional

class MovieCreate(BaseModel):
    title: str
    genre: str
    description: Optional[str] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    description: Optional[str]
    rating: float
    
    class Config:
        from_attributes = True