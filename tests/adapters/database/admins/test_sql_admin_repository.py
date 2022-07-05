import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.adapters.database.admins.model import Base
from app.adapters.database.admins.sql_admin_repository import SQLAdminRepository
from app.domain.admins.model.admin import Admin
from app.domain.admins.model.admin_id import AdminId
from tests.conf.config import settings_to_test


def get_admin_mock(admin_id) -> Admin:
    return Admin(
        id=admin_id, email='email@mail.com', firebase_id="aaa", first_name="Name", last_name="Lastname",
    )


class TestSQLAdminRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings_to_test.database_url)
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_admin_save(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository = SQLAdminRepository(self.session)
        admin_repository.save(admin)
        retrieved_admin = admin_repository.find_by_id(admin_id)
        assert retrieved_admin.id == admin.id

    def test_admin_repository_all(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin1 = get_admin_mock(admin_id)
        admin_repository.save(admin1)
        assert admin_repository.all() == [admin1]

    def test_admin_repository_all_filtered_by_email(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin1 = get_admin_mock(admin_id)
        admin_repository.save(admin1)
        assert admin_repository.all(email=admin1.email) == [admin1]

    def test_admin_repository_all_filtered_by_firebase_id(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin1 = get_admin_mock(admin_id)
        admin_repository.save(admin1)
        assert admin_repository.all(firebase_id=admin1.firebase_id) == [admin1]

    def test_admin_repository_all_filtered_empty(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin1 = get_admin_mock(admin_id)
        admin_repository.save(admin1)
        assert admin_repository.all(firebase_id='invalid id') == []

    def test_admin_repository_total(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"

        admin_repository.save(admin2)

        assert admin_repository.total() == 2

    def test_admin_repository_find_by_firebase_id(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)

        assert admin_repository.find_by_firebase_id(admin2.firebase_id) == admin2

    def test_admin_repository_find_by_email(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)

        assert admin_repository.find_by_email(admin2.email) == admin2

    def test_admin_repository_find_by_id(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)

        assert admin_repository.find_by_id(admin_id2) == admin2

    def test_admin_repository_find_by_id_not_found(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)

        assert admin_repository.find_by_id(AdminId(id=str(uuid.uuid4()))) is None

    def test_admin_repository_find_by_email_not_found(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)
        admin_repository.find_by_email("asd") is None

    def test_admin_repository_find_by_firebase_id_not_found(self):
        admin_repository = SQLAdminRepository(self.session)
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin = get_admin_mock(admin_id)
        admin_repository.save(admin)
        admin_id2 = AdminId(id=str(uuid.uuid4()))
        admin2 = get_admin_mock(admin_id2)
        admin2.firebase_id = "another id"
        admin2.email = "anothermail@mail.com"
        admin_repository.save(admin2)
        assert admin_repository.find_by_firebase_id("asd") is None
