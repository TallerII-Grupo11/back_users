import logging
from typing import List, Optional

from fastapi import Depends, APIRouter, status

from app.adapters.http.admin.input.admin import (
    AdminRequest,
    AdminUpdateRequest,
)
from app.adapters.http.admin.output.admin import AdminResponse
from app.dependencies.dependencies import admin_usecases_dependency
from app.domain.admins.usecases.admin import AdminUseCases

from app.domain.admins.query.admin_query import AdminQuery

router = APIRouter(tags=["admins"])
logger = logging.getLogger(__name__)


async def admin_query(
    firebase_id: Optional[str] = None,
    email: Optional[str] = None,
    admin_ids: Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
) -> AdminQuery:
    return AdminQuery(
        firebase_id=firebase_id,
        email=email,
        user_ids=admin_ids,
        offset=offset,
        limit=limit,
    )


@router.get(
    '/admins',
    response_model=List[AdminResponse],
    status_code=status.HTTP_200_OK,
)
async def get_admins(
    query: Optional[AdminQuery] = Depends(admin_query),
    admin_usecases: AdminUseCases = Depends(admin_usecases_dependency),
):
    logger.info("Get all admins called")
    return admin_usecases.list(query)


@router.post(
    '/admins',
    response_model=AdminResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_admins(
    admin_request: AdminRequest,
    admin_usecases: AdminUseCases = Depends(admin_usecases_dependency),
):
    logger.info("Create admin called")
    return admin_usecases.register(admin_request.to_create_admin_command())


@router.get(
    '/admins/{admin_id}',
    response_model=AdminResponse,
    status_code=status.HTTP_200_OK,
)
async def get_admin(
    admin_id: str,
    admin_usecases: AdminUseCases = Depends(admin_usecases_dependency),
):
    logger.info("Get admin by id called")
    admin = admin_usecases.find_by_id(admin_id)
    return admin


@router.put(
    '/admins/{admin_id}',
    response_model=AdminResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_admins(
    admin_id: str,
    admin_request: AdminUpdateRequest,
    admin_usecases: AdminUseCases = Depends(admin_usecases_dependency),
):
    logger.info("Update admin called")
    return admin_usecases.update(admin_request.to_update_admin_command(admin_id))
