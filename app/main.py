from fastapi import FastAPI, Depends
from .schemas import ListMoviesResponse, MovieItem, MovieCreate
from sqlalchemy.orm import Session
from .database import get_db
from .models import Movie

app = FastAPI(title="FastAPI with PostgresSQL and Alembic for YouTube")


@app.get("/")
def root():
    return {"message": "Welcome to my FastAPI app!"}


@app.get("/movies/", response_model=ListMoviesResponse)
def get_all_movies(db: Session = Depends(get_db)):
    all_movies = db.query(Movie).all()
    return {"movies": all_movies}


@app.get("/movie/{name}", response_model=ListMoviesResponse)
def get_movie_by_name(name:str, db: Session = Depends(get_db)):
    query = db.query(Movie)
    if name:
        query = query.filter(Movie.name.ilike(f"%{name}%"))
    all_movies = query.all()

    return {"movies": all_movies}



@app.post("/add_movie/", response_model=MovieItem)
def add_movie(newMovie: MovieCreate, db: Session = Depends(get_db)):
    new_db_movie = Movie(**newMovie.model_dump())
    db.add(new_db_movie)
    db.commit()
    db.refresh(new_db_movie)
    return new_db_movie
