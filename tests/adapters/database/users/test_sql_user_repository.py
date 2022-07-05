import unittest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.adapters.database.users.model import Base
from app.adapters.database.users.sql_user_repository import SQLUserRepository
from app.domain.users.model.user import User
from app.domain.users.model.user_id import UserId
from tests.conf.config import settings_to_test


def get_user_mock(user_id) -> User:
    return User(
        id=user_id, email='email@mail.com', firebase_id="aaa", first_name="Name", last_name="Lastname",
    )


class TestSQLUserRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings_to_test.database_url)
        self.session = Session(self.engine)
        Base.metadata.create_all(self.engine)
        self.session.commit()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_user_save(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository = SQLUserRepository(self.session)
        user_repository.save(user)
        retrieved_user = user_repository.find_by_id(user_id)
        assert retrieved_user.id == user.id

    def test_user_repository_all(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user1 = get_user_mock(user_id)
        user_repository.save(user1)
        assert user_repository.all() == [user1]

    def test_user_repository_all_filtered_by_email(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user1 = get_user_mock(user_id)
        user_repository.save(user1)
        assert user_repository.all(email=user1.email) == [user1]

    def test_user_repository_all_filtered_by_firebase_id(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user1 = get_user_mock(user_id)
        user_repository.save(user1)
        assert user_repository.all(firebase_id=user1.firebase_id) == [user1]

    def test_user_repository_all_filtered_by_user_ids(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user1 = get_user_mock(user_id)
        user_repository.save(user1)
        assert user_repository.all(user_ids=user_id.id) == [user1]

    def test_user_repository_all_filtered_empty(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user1 = get_user_mock(user_id)
        user_repository.save(user1)
        assert user_repository.all(firebase_id='invalid id') == []

    def test_user_repository_total(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"

        user_repository.save(user2)

        assert user_repository.total() == 2

    def test_user_repository_find_by_firebase_id(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)

        assert user_repository.find_by_firebase_id(user2.firebase_id) == user2

    def test_user_repository_find_by_email(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)

        assert user_repository.find_by_email(user2.email) == user2

    def test_user_repository_find_by_id(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)

        assert user_repository.find_by_id(user_id2) == user2

    def test_user_repository_find_by_id_not_found(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)

        assert user_repository.find_by_id(UserId(id=str(uuid.uuid4()))) is None

    def test_user_repository_find_by_email_not_found(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)
        assert user_repository.find_by_email("asd") is None

    def test_user_repository_find_by_firebase_id_not_found(self):
        user_repository = SQLUserRepository(self.session)
        user_id = UserId(id=str(uuid.uuid4()))
        user = get_user_mock(user_id)
        user_repository.save(user)
        user_id2 = UserId(id=str(uuid.uuid4()))
        user2 = get_user_mock(user_id2)
        user2.firebase_id = "another id"
        user2.email = "anothermail@mail.com"
        user_repository.save(user2)
        assert user_repository.find_by_firebase_id("asd") is None
