class UserAlreadyExistsError(Exception):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value


class InvalidCredentialsError(Exception):
    """Raised when authentication fails."""
    pass
