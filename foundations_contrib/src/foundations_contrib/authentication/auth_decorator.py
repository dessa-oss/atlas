# /server.py

from functools import wraps

from flask import request, _request_ctx_stack
from jose import jwt

from foundations_core_rest_api_components.exceptions import AuthError
from .authentication_client import AuthenticationClient


def get_token_from_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    if len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    if len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be 'Bearer <token>'",
            },
            401,
        )

    token = parts[1]
    return token


def requires_auth(auth_client: AuthenticationClient):
    """Determines if the Access Token is valid."""

    def decorator(func):
        @wraps(func)
        def verify(*args, **kwargs):
            token = get_token_from_header()
            jwks = auth_client.json_web_key_set
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=["RS256"],
                        audience="account",
                        issuer=auth_client.metadata['issuer'],
                    )
                except jwt.ExpiredSignatureError:
                    raise AuthError(
                        {"code": "token_expired", "description": "Token is expired."},
                        401,
                    )
                except jwt.JWTClaimsError as exc:
                    raise AuthError(
                        {
                            "code": "invalid_claims",
                            "description": "Incorrect claims, please check the audience and issuer.",
                        },
                        401,
                    )
                except Exception as exc:
                    raise AuthError(
                        {
                            "code": "invalid_header",
                            "description": "Unable to parse authentication token.",
                        },
                        401,
                    )

                _request_ctx_stack.top.current_user = payload
                return func(*args, **kwargs)
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to find appropriate key.",
                },
                401,
            )

        return verify

    return decorator


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_from_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False
