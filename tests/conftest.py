from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer  # type: ignore
from app.database import Base, get_db
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.models import Movie
from datetime import date


@pytest.fixture(scope='session')
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope='function')
def db_session(postgres_container: PostgresContainer):
    conn_url: str = postgres_container.get_connection_url()  # type: ignore
    assert isinstance(conn_url, str)
    engine = create_engine(conn_url)

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture(scope='function')
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


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
