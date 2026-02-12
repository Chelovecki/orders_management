from uuid import UUID


# User
class UserAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value


class UserNotFoundError(Exception):
    """Raised when user request to non-existing order or not his own order"""

    def __init__(self, user_id: int):
        self.user_id = user_id


# Auth
class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""


# Order
class OrderNotFoundError(Exception):
    """Raised when user request to non-existing order or not his own order"""

    def __init__(self, order_id: UUID):
        self.order_id = order_id
