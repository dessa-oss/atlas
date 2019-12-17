"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 11 2018
"""

# TODO: change back to "auth-server-url": "http://foundations-authentication-server:8080/auth",

ATLAS = {
    "realm": "Atlas",
    "auth-server-url": "http://localhost:8080/auth",
    "ssl-required": "none",
    "resource": "foundations",
    "public-client": True,
    "verify-token-audience": True,
    "use-resource-role-mappings": True,
    "confidential-port": 0
}
