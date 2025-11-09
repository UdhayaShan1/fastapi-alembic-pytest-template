from pydantic import BaseModel
from datetime import date
from typing import List


class MovieItem(BaseModel):
    id: int
    name: str
    release_date: date | None = None
    rating: float | None = None

    class Config:
        from_attributes = True


class MovieCreate(BaseModel):
    name: str
    release_date: date | None = None
    rating: float | None = None


class ListMoviesResponse(BaseModel):
    movies: List[MovieItem]
