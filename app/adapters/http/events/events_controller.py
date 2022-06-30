import logging

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from app.adapters.http.events.input.events import LoginRequest
from app.adapters.rest.queue_metrics_client import QueueMetricsClient
from app.datadog.datadog_metrics import DataDogMetric
from app.dependencies.dependencies import get_restclient_metrics

router = APIRouter(tags=["events"])
logger = logging.getLogger(__name__)


@router.post(
    '/login',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def notify_login(
    login_request: LoginRequest,
    rest_metrics: QueueMetricsClient = Depends(get_restclient_metrics),
):
    if login_request.federated:
        DataDogMetric.new_login_federated()
    else:
        DataDogMetric.new_login()

    try:
        rest_metrics.record_login(login_request.federated)
    except Exception as e:
        logger.error("Error in Queue Metrics request: ", e)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/password_reset',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def notify_password_reset(
    rest_metrics: QueueMetricsClient = Depends(get_restclient_metrics),
):
    DataDogMetric.password_reset()

    try:
        rest_metrics.record_password_reset()
    except Exception as e:
        logger.error("Error in Queue Metrics request: ", e)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
