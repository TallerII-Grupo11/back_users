import unittest
import uuid

from unittest.mock import MagicMock

from app.domain.users.command.user_create_command import UserCreateCommand
from app.domain.users.command.user_update_command import UserUpdateCommand
from app.domain.users.command.user_update_role_command import UpdateUserRoleCommand
from app.domain.users.command.user_update_status_command import UpdateUserStatusCommand
from app.domain.users.model.user import User, UserStatus, UserRole
from app.domain.users.model.user_exceptions import UserAlreadyExistException, UsersNotFoundError
from app.domain.users.model.user_id import UserId
from app.domain.users.query.user_query import UserQuery
from app.domain.users.usecases.user import UserUseCases


def get_user_mock(user_id) -> User:
    return User(
        id=user_id, email='email@mail.com', firebase_id="aaa", first_name="Name", last_name="Lastname",
    )


class TestUserUseCases(unittest.TestCase):
    user_uow = MagicMock()
    firebase = MagicMock()
    rest_metrics = MagicMock()

    def test_list_empty(self):
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        self.user_uow.repository.all = MagicMock(return_value=[])
        user_query = UserQuery()
        self.assertEqual([], user_use_cases.list(user_query))

    def test_list_with_results(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        self.user_uow.repository.all = MagicMock(return_value=[user_mock])
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_query = UserQuery()
        self.assertEqual([user_mock], user_use_cases.list(user_query))

    def test_list_with_filtered_results(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        self.user_uow.repository.all = MagicMock(return_value=[user_mock])
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_query = UserQuery(q='mock')
        self.assertEqual([user_mock], user_use_cases.list(user_query))

    def test_register(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)

        self.user_uow.repository.find_by_email = MagicMock(return_value=None)
        self.user_uow.repository.find_by_firebase_id = MagicMock(return_value=None)
        self.user_uow.repository.save = MagicMock(return_value=user_mock)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_register = UserCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertIsNotNone(user_use_cases.register(user_register))

    def test_register_duplicate_username(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        previous_user_mock = get_user_mock(user_id)
        previous_user_mock.firebase_id = "something"
        self.user_uow.repository.find_by_email = MagicMock(return_value=previous_user_mock)
        self.user_uow.repository.save = MagicMock(return_value=user_mock)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_register = UserCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertRaises(
            UserAlreadyExistException, user_use_cases.register, user_register
        )

    def test_register_duplicate_firebase_id(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        previous_user_mock = get_user_mock(user_id)
        previous_user_mock.email = "different@mail.com"
        self.user_uow.repository.find_by_email = MagicMock(return_value=None)
        self.user_uow.repository.find_by_firebase_id = MagicMock(return_value=previous_user_mock)
        self.user_uow.repository.save = MagicMock(return_value=user_mock)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_register = UserCreateCommand(
            email='email@mail.com', first_name="Name", last_name="Lastname", firebase_id="aaa"
        )
        self.assertRaises(
            UserAlreadyExistException, user_use_cases.register, user_register
        )

    def test_find_by_id(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        self.assertEqual(user_mock, user_use_cases.find_by_id(user_id.id))

    def test_update_user_status_to_blocked(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        user_mock.status = UserStatus.ACTIVE
        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.firebase.update_user = MagicMock(return_value=None)
        self.rest_metrics.record_user_blocked = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        command = UpdateUserStatusCommand(
            user_id=user_id.id, status=UserStatus.BLOCKED.value
        )
        updated_user = user_use_cases.update_status(command)
        assert updated_user.is_blocked()

    def test_update_user_status_user_not_found(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        user_mock.status = UserStatus.ACTIVE
        self.user_uow.repository.find_by_id = MagicMock(return_value=None)
        self.firebase.update_user = MagicMock(return_value=None)
        self.rest_metrics.record_user_blocked = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        command = UpdateUserStatusCommand(
            user_id=user_id.id, status=UserStatus.BLOCKED.value
        )
        self.assertRaises(
            UsersNotFoundError, user_use_cases.update_status, command
        )

    def test_update_user_status_to_active(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        user_mock.status = UserStatus.BLOCKED
        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.firebase.update_user = MagicMock(return_value=None)
        self.rest_metrics.record_user_blocked = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        command = UpdateUserStatusCommand(
            user_id=user_id.id, status=UserStatus.ACTIVE.value
        )
        updated_user = user_use_cases.update_status(command)
        assert not updated_user.is_blocked()

    def test_update_user_role_to_artist(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        user_mock.role = UserRole.LISTENER
        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.firebase.update_user = MagicMock(return_value=None)
        self.rest_metrics.record_user_blocked = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        command = UpdateUserRoleCommand(
            user_id=user_id.id, role=UserRole.ARTIST.value
        )
        updated_user = user_use_cases.update_role(command)
        assert updated_user.is_artist()

    def test_update_user_role_to_listener(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)
        user_mock.role = UserRole.ARTIST
        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.firebase.update_user = MagicMock(return_value=None)
        self.rest_metrics.record_user_blocked = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        command = UpdateUserRoleCommand(
            user_id=user_id.id, role=UserRole.LISTENER.value
        )
        updated_user = user_use_cases.update_role(command)
        assert not updated_user.is_artist()

    def test_update(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)

        self.user_uow.repository.find_by_id = MagicMock(return_value=user_mock)
        self.firebase.update_user = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_update = UserUpdateCommand(
            user_id=user_id.id, email='email@mail.com', first_name="different", last_name="something",
            firebase_id="aaa", status=UserStatus.BLOCKED,
        )
        self.assertIsNotNone(user_use_cases.update(user_update))

    def test_update_not_found(self):
        user_id = UserId(id=str(uuid.uuid4()))
        user_mock = get_user_mock(user_id)

        self.user_uow.repository.find_by_id = MagicMock(return_value=None)
        user_use_cases = UserUseCases(self.user_uow, self.firebase, self.rest_metrics)
        user_update = UserUpdateCommand(
            user_id=user_id.id, email='email@mail.com', first_name="different", last_name="something",
            firebase_id="aaa", status=UserStatus.BLOCKED,
        )
        self.assertRaises(
            UsersNotFoundError, user_use_cases.update, user_update
        )
