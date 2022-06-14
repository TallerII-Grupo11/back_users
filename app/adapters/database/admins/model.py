from typing import Union

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.adapters.database.database import get_declarative_base
from app.domain.admins.model.admin import Admin, AdminStatus
from app.domain.admins.model.admin_id import AdminId

Base = get_declarative_base()


class AdminDTO(Base):
    __tablename__ = "admins"

    id: Union[str, Column] = Column(String, primary_key=True, index=True)
    firebase_id: Union[str, Column] = Column(String, unique=True, index=True)
    email: Union[str, Column] = Column(String, unique=True, index=True)
    first_name: Union[str, Column] = Column(String)
    last_name: Union[str, Column] = Column(String)
    status: Union[str, Column] = Column(String, default=True)
    created_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Union[DateTime, Column] = Column(
        DateTime(timezone=True), onupdate=func.now()
    )

    @staticmethod
    def from_entity(user: Admin) -> "AdminDTO":
        return AdminDTO(
            id=user.id.id,
            firebase_id=user.firebase_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            status=user.status,
        )

    def to_entity(self) -> Admin:
        return Admin(
            id=AdminId(self.id),
            firebase_id=self.firebase_id,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            status=AdminStatus(self.status),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
