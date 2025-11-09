from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Movie


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




