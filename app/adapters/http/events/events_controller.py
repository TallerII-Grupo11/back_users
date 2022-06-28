from fastapi import APIRouter, status
from fastapi.responses import Response

from app.adapters.http.events.input.events import LoginRequest
from app.datadog.datadog_metrics import DataDogMetric

router = APIRouter(tags=["events"])


@router.post(
    '/login',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def notify_login(
    login_request: LoginRequest,
):
    if login_request.federated:
        DataDogMetric.new_login_federated()
    else:
        DataDogMetric.new_login()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/password_reset',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def notify_password_reset():
    DataDogMetric.password_reset()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
