from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.adapters.database.admins.model import AdminDTO
from app.domain.admins.model.admin import Admin
from app.domain.admins.model.admin_id import AdminId
from app.domain.admins.repository.admin_repository import AdminRepository


class SQLAdminRepository(AdminRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def save(self, admin: Admin):
        admin_dto = AdminDTO.from_entity(admin)
        try:
            self.session.add(admin_dto)
        except Exception:
            raise

    def update(self, admin: Admin):
        try:
            self.session.query(AdminDTO).filter_by(id=admin.id.id).update(
                {
                    AdminDTO.firebase_id: admin.firebase_id,
                    AdminDTO.first_name: admin.first_name,
                    AdminDTO.last_name: admin.last_name,
                    AdminDTO.email: admin.email,
                    AdminDTO.status: str(admin.status.value),
                }
            )

        except Exception:
            raise

    def find_by_id(self, admin_id: AdminId) -> Admin:
        try:
            admin_dto = self.session.query(AdminDTO).filter_by(id=admin_id.id).one()
        except NoResultFound:
            return None
        except Exception:
            raise
        return admin_dto.to_entity()

    def find_by_email(self, email: str) -> Admin:
        try:
            admin_dto = self.session.query(AdminDTO).filter_by(email=email).one()
        except NoResultFound:
            return None
        except Exception:
            raise
        return admin_dto.to_entity()

    def all(
        self,
        firebase_id: Optional[str] = None,
        email: Optional[str] = None,
        user_ids: Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Admin]:
        query = self.session.query(AdminDTO)
        if user_ids:
            user_ids_list = user_ids.split(',')
            query = query.where(AdminDTO.id.in_(user_ids_list))
        if firebase_id:
            query = query.filter_by(firebase_id=firebase_id)
        if email:
            query = query.filter(AdminDTO.email == email)
        if firebase_id and email:
            query = query.filter(AdminDTO.firebase_id == firebase_id).filter(
                AdminDTO.email == email
            )

        return [u.to_entity() for u in query.limit(limit).offset(offset)]

    def total(self) -> int:
        return self.session.query(AdminDTO).count()
