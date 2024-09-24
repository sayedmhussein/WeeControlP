import datetime
import functools
from datetime import timezone
import jwt
from pydantic import BaseModel


def get_jwt(claims: dict):
    if claims is None:
        claims = {}
    claims = dict(claims)
    claims['iat'] = datetime.datetime.now(tz=timezone.utc)
    claims['exp'] = datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=15)
    claims['iss'] = 'WeeControl'
    return jwt.encode(claims, "secret", algorithm="HS256")


def get_claims(encoded_jwt: str):
    options = {'require': ["iat", "exp", "iss"], 'verify_signature': True}
    try:
        claims = jwt.decode(encoded_jwt, "secret", options=options, algorithms=["HS256"])
        return claims
    except jwt.ExpiredSignatureError:
        return None
    except [jwt.exceptions.InvalidTokenError, jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError,
            jwt.exceptions.InvalidAudienceError, jwt.exceptions.InvalidIssuerError,
            jwt.exceptions.InvalidIssuedAtError, jwt.exceptions.ImmatureSignatureError,
            jwt.exceptions.InvalidKeyError, jwt.exceptions.InvalidAlgorithmError,
            jwt.exceptions.MissingRequiredClaimError]:
        return None
    except jwt:
        return None