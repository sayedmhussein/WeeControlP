import functools
from fastapi import Request, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from server.services.secuity import get_claims


def authorize(claims: dict = None):
    def decorator(func):
        @functools.wraps(func)
        async def authorize_function(*args, **kwargs):
            request: Request = kwargs["request"]
            token = request.state.token
            # token = request.cookies.get("token")
            if token is None:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No valid token found")
            c = get_claims(token)
            if c is None:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No valid token found")

            if claims is None or len(claims) < 1:
                return await func(*args, **kwargs)

            if claims_approved(claims, c):
                return await func(*args, **kwargs)
            else:
                raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User don't have right to access the resource")
        return authorize_function
    return decorator

def claims_approved(required: dict, have: dict) -> bool:
    return True