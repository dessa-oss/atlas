
from foundations_authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_authentication.utils import get_token_from_header


def is_string(string):
    return isinstance(string, str)
