
from functools import wraps

from jose import jwt

from foundations_authentication.authentication_client import AuthenticationClient
from foundations_authentication.utils import get_token_from_header, verify_token


def requires_auth(auth_client: AuthenticationClient):
    """Determines if the Access Token is valid."""

    def decorator(func):
        @wraps(func)
        def verify(*args, **kwargs):
            token = get_token_from_header()
            jwks = auth_client.json_web_key_set
            issuer = auth_client.issuer
            verify_token(token, jwks, issuer)
            return func(*args, **kwargs)

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
