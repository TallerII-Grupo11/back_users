import unittest
import httpx
import respx

from app.adapters.rest.dtos.metric import MetricResponseDto
from app.adapters.rest.queue_metrics_client import QueueMetricsClient


def get_mocked_response(status_code: int, mock: MetricResponseDto) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=mock.dict(),
    )


class TestQueueMetricsClient(unittest.TestCase):
    test_url = "https://test-api.com"

    @respx.mock
    def test_login(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/login?federated=False").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_login(federated=False)

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_login_federated(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/login?federated=True").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_login(federated=True)

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_new_user(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/users?federated=False").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_new_user(federated=False)

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_new_user_federated(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/users?federated=True").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_new_user(federated=True)

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_block_user(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/blocked").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_user_blocked()

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_password_reset(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/password_reset").mock(
            return_value=get_mocked_response(200, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        dto = client.record_password_reset()

        assert dto.id == "id"
        assert dto.name == "name"

    @respx.mock
    def test_password_reset_error(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/password_reset").mock(
            return_value=get_mocked_response(500, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        self.assertRaises(
            Exception, client.record_password_reset
        )

    @respx.mock
    def test_user_blocked_error(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/blocked").mock(
            return_value=get_mocked_response(500, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        self.assertRaises(
            Exception, client.record_user_blocked
        )

    @respx.mock
    def test_login_error(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/login").mock(
            return_value=get_mocked_response(500, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        self.assertRaises(
            Exception, client.record_login
        )

    @respx.mock
    def test_login_error(self, respx_mock):
        mocked_metric_response = MetricResponseDto(id="id", name="name")
        respx_mock.post(f"{self.test_url}/users").mock(
            return_value=get_mocked_response(500, mocked_metric_response))
        client = QueueMetricsClient(self.test_url)
        self.assertRaises(
            Exception, client.record_new_user
        )
