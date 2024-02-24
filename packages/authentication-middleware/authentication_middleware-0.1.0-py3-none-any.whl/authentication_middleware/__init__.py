from functools import wraps
from inspect import iscoroutinefunction
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette import status


def scope(*scopes: str):

    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request):
            print(f"Checking if user has the right scope {scopes}")
            for s in scopes:
                if s not in request.state.user["scopes"].split(" "):
                    raise HTTPException(
                        detail="Unauthorized Request scope",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    )
            if iscoroutinefunction(func):
                return await func(request)
            else:
                return func(request)

        return wrapper

    return decorator
