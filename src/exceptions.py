class UserAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value


class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""
    pass


class OrderNotFoundError(Exception):
    """Raised when user request to non-existing order or not his own order"""

    def __init__(self, order_id: int):
        self.order_id = order_id
