from typing import Any, Awaitable, Callable, MutableMapping
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from starlette.requests import Request
from starlette.responses import Response
from starlette.exceptions import HTTPException
from starlette import status
from jose import jwt
from jose.exceptions import JWTError
from starlette.types import ASGIApp

"""
    check if authorization header is present
    
    decode the authorization header and check if the user is valid

    if "Authorization" not in request.headers:
    
    Authorization: "Bearer ahfkfawhjefahjkdfkasjkef"
    lopit
"""

SECRET_KEY = "mysecretkey"
SECRET_PAYLOAD = "topsecret"


class AuthenticationMiddleware(BaseHTTPMiddleware):

    def __init__(
        self,
        app: Callable[
            [
                MutableMapping[str, Any],
                Callable[[], Awaitable[MutableMapping[str, Any]]],
                Callable[[MutableMapping[str, Any]], Awaitable[None]],
            ],
            Awaitable[None],
        ],
        dispatch: (
            Callable[
                [Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]
            ]
            | None
        ) = None,
        secret_key: str = SECRET_KEY,
        secret_payload: str = SECRET_PAYLOAD,
    ) -> None:
        super().__init__(app, dispatch)
        self.secret_key = secret_key
        self.secret_payload = secret_payload

    async def dispatch(self, request: Request, call_next) -> Response:

        try:
            bearer, token = request.headers.get("Authorization", "").split(" ")
        except ValueError:
            raise HTTPException(
                detail="Unauthorized Request", status_code=status.HTTP_401_UNAUTHORIZED
            )

        if bearer.lower() != "bearer":
            raise HTTPException(
                detail="Unauthorized Request", status_code=status.HTTP_401_UNAUTHORIZED
            )

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            raise HTTPException(
                detail="Unauthorized Request", status_code=status.HTTP_401_UNAUTHORIZED
            )

        if decoded_token.get("secret_payload", "") != SECRET_PAYLOAD:
            raise HTTPException(
                detail="Unauthorized Request", status_code=status.HTTP_401_UNAUTHORIZED
            )

        request.state.user = decoded_token

        return await call_next(request)
