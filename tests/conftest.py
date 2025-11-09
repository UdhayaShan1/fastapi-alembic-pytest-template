from sqlalchemy import create_engine
import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer 
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
    conn_url: str = postgres_container.get_connection_url() 
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


