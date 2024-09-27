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
    """

    :param required: contains the dict of claims which must exist.
    :param have: contains the user claims.
    :return: True if the user have all the required claims.
    """
    if len(required) > 0:
        for c in required:
            key = c.strip()
            if key not in have.keys():
                return False
            if len(required[c]) > 0:
                value: str = required[c].strip()
                if "||" in value and "&&" in value:
                    raise "Not Support to have both || and && at same claim value"
                elif "||" in value:
                    values = value.split("||")
                    for v in values:
                        if have[key] == v.strip():
                            break
                        if v == values[-1]:
                            return False
                elif "&&" in value:
                    values = value.split("||")
                    for v in values:
                        if have[key] != v.strip():
                            return False
                else:
                    for v in required[c].strip().split("||"):
                        if required[c].strip() != have[c].strip():
                            return False

    return True