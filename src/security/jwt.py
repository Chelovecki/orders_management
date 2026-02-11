from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from src.exceptions import InvalidCredentialsError
from src.settings import JWT


def create_access_token(subject: str, expires_delta: timedelta | None = None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=15)

    payload = {
        "sub": subject,
        "exp": datetime.now(timezone.utc) + expires_delta,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(payload, JWT.SECRET, algorithm=JWT.ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, JWT.SECRET, algorithms=[JWT.ALGORITHM])

    except InvalidTokenError:  # общая ошибка на все случаи
        raise InvalidCredentialsError()
