from app.conf.config import Settings

settings_to_test = Settings(
    environment="test",
    title="Test",
    description="Test",
    version="1.0",
    database_url="sqlite:///:memory:",
    secret_key="test",
    algorithm="HS256",
    version_prefix="/v1",
    firebase_project_id="test",
    firebase_private_key="test",
    firebase_private_key_id="test",
    firebase_client_email="test",
    firebase_client_id=123,
    firebase_client_cert_url="test",
    firebase_storage_bucket="test",
    queue_metrics_url="http://test-api.com",
)