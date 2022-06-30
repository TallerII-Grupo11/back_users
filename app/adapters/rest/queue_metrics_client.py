import httpx

from app.adapters.rest.dtos.metric import MetricResponseDto


class QueueMetricsClient:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def record_login(self, federated: bool) -> MetricResponseDto:
        r = httpx.post(f'{self.api_url}/login?federated={federated}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        return MetricResponseDto(**r.json())

    def record_new_user(self, federated: bool) -> MetricResponseDto:
        r = httpx.post(f'{self.api_url}/users?federated={federated}')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        return MetricResponseDto(**r.json())

    def record_password_reset(self) -> MetricResponseDto:
        r = httpx.post(f'{self.api_url}/password_reset')
        if r.status_code != httpx.codes.OK:
            r.raise_for_status()

        return MetricResponseDto(**r.json())
