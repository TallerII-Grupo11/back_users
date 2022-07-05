from unittest.mock import MagicMock

from app.adapters.http.events.input.events import LoginRequest
from tests.adapters.http.bootstrap_app import test_app, mocked_metrics_client


def test_login_event(test_app: test_app):
    login_request = LoginRequest(federated=False)
    response = test_app.post("/login", json=login_request.dict())
    mocked_metrics_client.record_login = MagicMock(return_value=None)
    assert response.status_code == 204


def test_password_reset_event(test_app: test_app):
    response = test_app.post("/password_reset")
    mocked_metrics_client.record_password_reset = MagicMock(return_value=None)
    assert response.status_code == 204
