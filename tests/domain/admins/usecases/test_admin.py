import unittest
import uuid

from unittest.mock import MagicMock

from app.domain.admins.command.admin_create_command import AdminCreateCommand
from app.domain.admins.command.admin_update_command import AdminUpdateCommand
from app.domain.admins.model.admin import Admin, AdminStatus
from app.domain.admins.model.admin_exceptions import AdminAlreadyExistException, AdminsNotFoundError
from app.domain.admins.model.admin_id import AdminId
from app.domain.admins.query.admin_query import AdminQuery
from app.domain.admins.usecases.admin import AdminUseCases


def get_admin_mock(admin_id) -> Admin:
    return Admin(
        id=admin_id, email='email@mail.com', firebase_id="aaa", first_name="Name", last_name="Lastname",
    )


class TestAdminUseCases(unittest.TestCase):
    admin_uow = MagicMock()
    firebase = MagicMock()

    def test_list_empty(self):
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        self.admin_uow.repository.all = MagicMock(return_value=[])
        admin_query = AdminQuery()
        self.assertEqual([], admin_use_cases.list(admin_query))

    def test_list_with_results(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)
        self.admin_uow.repository.all = MagicMock(return_value=[admin_mock])
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_query = AdminQuery()
        self.assertEqual([admin_mock], admin_use_cases.list(admin_query))

    def test_list_with_filtered_results(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)
        self.admin_uow.repository.all = MagicMock(return_value=[admin_mock])
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_query = AdminQuery(q='mock')
        self.assertEqual([admin_mock], admin_use_cases.list(admin_query))

    def test_register(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)

        self.admin_uow.repository.find_by_email = MagicMock(return_value=None)
        self.admin_uow.repository.find_by_firebase_id = MagicMock(return_value=None)
        self.admin_uow.repository.save = MagicMock(return_value=admin_mock)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_register = AdminCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertIsNotNone(admin_use_cases.register(admin_register))

    def test_register_duplicate_username(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)
        previous_admin_mock = get_admin_mock(admin_id)
        previous_admin_mock.firebase_id = "something"
        self.admin_uow.repository.find_by_email = MagicMock(return_value=previous_admin_mock)
        self.admin_uow.repository.save = MagicMock(return_value=admin_mock)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_register = AdminCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertRaises(
            AdminAlreadyExistException, admin_use_cases.register, admin_register
        )

    def test_register_duplicate_firebase_id(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)
        previous_admin_mock = get_admin_mock(admin_id)
        previous_admin_mock.email = "different@mail.com"
        self.admin_uow.repository.find_by_email = MagicMock(return_value=None)
        self.admin_uow.repository.find_by_firebase_id = MagicMock(return_value=previous_admin_mock)
        self.admin_uow.repository.save = MagicMock(return_value=admin_mock)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_register = AdminCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertRaises(
            AdminAlreadyExistException, admin_use_cases.register, admin_register
        )

    def test_find_by_id(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)
        self.admin_uow.repository.find_by_id = MagicMock(return_value=admin_mock)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        self.assertEqual(admin_mock, admin_use_cases.find_by_id(admin_id.id))

    def test_update(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)

        self.admin_uow.repository.find_by_id = MagicMock(return_value=admin_mock)
        self.firebase.update_admin = MagicMock(return_value=None)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_update = AdminUpdateCommand(
            admin_id=admin_id.id, email='email@mail.com', first_name="different", last_name="something",
            firebase_id="aaa", status=AdminStatus.BLOCKED,
        )
        self.assertIsNotNone(admin_use_cases.update(admin_update))

    def test_update_not_found(self):
        admin_id = AdminId(id=str(uuid.uuid4()))
        admin_mock = get_admin_mock(admin_id)

        self.admin_uow.repository.find_by_id = MagicMock(return_value=None)
        admin_use_cases = AdminUseCases(self.admin_uow, self.firebase)
        admin_update = AdminUpdateCommand(
            admin_id=admin_id.id, email='email@mail.com', first_name="different", last_name="something",
            firebase_id="aaa", status=AdminStatus.BLOCKED,
        )
        self.assertRaises(
            AdminsNotFoundError, admin_use_cases.update, admin_update
        )

