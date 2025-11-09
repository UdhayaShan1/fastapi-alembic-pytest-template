from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Movie
import pytest
from datetime import date

@pytest.fixture(scope='function')
def sample_movie_data(db_session: Session):
    movies: list[Movie] = [
        Movie(
            name="Inception",
            release_date=date(2010, 7, 16),
            rating=8.8
        ),
        Movie(
            name="The Dark Knight",
            release_date=date(2008, 7, 18),
            rating=9.0
        ),
        Movie(
            name="Interstellar",
            release_date=date(2014, 11, 7),
            rating=8.6
        ),
        Movie(
            name="The Matrix",
            release_date=date(1999, 3, 31),
            rating=8.7
        ),
        Movie(
            name="Pulp Fiction",
            release_date=date(1994, 10, 14),
            rating=8.9
        ),
    ]

    db_session.add_all(movies)
    db_session.commit()


def test_get_all_movies(client: TestClient, sample_movie_data):
    """Test getting all movies from the database"""
    response = client.get("/movies/")
    assert response.status_code == 200

    data = response.json()
    expected_names = {"Inception", "The Dark Knight", "Interstellar", "The Matrix", "Pulp Fiction"}

    retrieved_names = {movie['name'] for movie in data['movies']}

    assert expected_names == retrieved_names

def test_get_all_movies_crud(client: TestClient, db_session: Session, sample_movie_data):
    response = client.get("/movies/")

    assert response.status_code == 200

    db_results = db_session.query(Movie).all()
    expected_names = {"Inception", "The Dark Knight", "Interstellar", "The Matrix", "Pulp Fiction"}
    retrieved_names = {movie.name for movie in db_results}
    assert expected_names == retrieved_names




