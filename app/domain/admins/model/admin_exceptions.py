class AdminsNotFoundError(Exception):
    def __init__(self, admin_id: str):
        self.message = f'Admin {admin_id} not found'

    def __str__(self):
        return self.message


class AdminAlreadyExistException(Exception):
    message = "This Admin already exists"

    def __str__(self):
        return AdminAlreadyExistException.message


class AdminsBlockedException(Exception):
    message = "This Admin is blocked."

    def __str__(self):
        return AdminsBlockedException.message
