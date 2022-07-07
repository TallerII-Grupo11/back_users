import os
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.database.users.model import Base, UserDTO
from app.adapters.database.admins.model import AdminDTO
from app.dependencies.dependencies import get_session, firebase_service_dependency, get_restclient_metrics
from app.dependencies.dependencies import get_settings
from tests.conf.config import settings_to_test


def build_test_db_context():
    engine = create_engine(
        settings_to_test.database_url, connect_args={"check_same_thread": False}
    )
    UserDTO.__table__.create(bind=engine, checkfirst=True)
    AdminDTO.__table__.create(bind=engine, checkfirst=True)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    return session()


TestingSessionLocal = build_test_db_context()

mocked_metrics_client = MagicMock()


def override_get_session():
    try:
        yield TestingSessionLocal
    finally:
        TestingSessionLocal.close()


def override_get_settings():
    return settings_to_test


def override_validate():
    return True


def override_firebase():
    return MagicMock()


def override_restclient_metrics():
    return mocked_metrics_client


@pytest.fixture(scope="module")
def test_app():
    # Override environment variables to run TestClient app
    os.environ = settings_to_test.dict()
    from app import main

    client = TestClient(main.app)
    main.app.dependency_overrides[get_settings] = override_get_settings
    main.app.dependency_overrides[get_session] = override_get_session
    main.app.dependency_overrides[firebase_service_dependency] = override_firebase
    main.app.dependency_overrides[get_restclient_metrics] = override_restclient_metrics

    yield client  # testing happens here