class UsersNotFoundError(Exception):
    def __init__(self, user_id: str):
        self.message = f'User {user_id} not found'

    def __str__(self):
        return self.message


class UserAlreadyExistException(Exception):
    message = "This User already exists"

    def __str__(self):
        return UserAlreadyExistException.message


class UserAlreadyHadStatusError(Exception):
    message = "This User already had this status."

    def __str__(self):
        return UserAlreadyHadStatusError.message


class UserAlreadyHadRoleError(Exception):
    message = "This User already had this role."

    def __str__(self):
        return UserAlreadyHadRoleError.message


class UsersBlockedException(Exception):
    message = "This User is blocked."

    def __str__(self):
        return UsersBlockedException.message


class InvalidCredentialsError(Exception):
    message = "Invalid user credentials"

    def __str__(self):
        return InvalidCredentialsError.message
