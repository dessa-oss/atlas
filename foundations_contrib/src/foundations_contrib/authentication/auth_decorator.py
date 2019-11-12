"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

from functools import wraps

from jose import jwt

from foundations_contrib.authentication.authentication_client import AuthenticationClient
from foundations_contrib.authentication.utils import get_token_from_header, verify_token


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



# # Dev purposes
# from flask import Flask, jsonify
# from flask_cors import cross_origin

# from foundations_core_rest_api_components.exceptions import AuthError
# from foundations_contrib.authentication.configs import ATLAS

# client = AuthenticationClient(ATLAS, redirect_url="/api/v2beta/auth")

# APP = Flask(__name__)

# # This doesn't need authentication
# @APP.route("/api/public")
# @cross_origin(headers=["Content-Type", "Authorization"])
# def public():
#     response = (
#         "Hello from a public endpoint! You don't need to be authenticated to see this."
#     )
#     return jsonify(message=response)


# # This needs authentication
# @APP.route("/api/private")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth(client)
# def private():
#     response = (
#         "Hello from a private endpoint! You need to be authenticated to see this."
#     )
#     return jsonify(message=response)


# # This needs authorization
# @APP.route("/api/private-scoped")
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth(client)
# def private_scoped():
#     if requires_scope("profile"):
#         response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
#         return jsonify(message=response)
#     raise AuthError(
#         {
#             "code": "Unauthorized",
#             "description": "You don't have access to this resource",
#         },
#         403,
#     )

# @APP.errorhandler(AuthError)
# def handle_auth_error(exc):
#     response = jsonify(exc.error)
#     response.status_code = exc.status_code
#     return response

# APP.run()
