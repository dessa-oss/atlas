"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""

import requests

import google.auth as auth
import google.auth.transport as transport

# adapted from google cloud storage
class AuthorizedStorageSession(object):
    def __init__(self, max_retries, pool_block, pool_size):
        refresh_status_codes=transport.DEFAULT_REFRESH_STATUS_CODES
        max_refresh_attempts=transport.DEFAULT_MAX_REFRESH_ATTEMPTS
        refresh_timeout=None

        credentials, _ = auth.default()

        SCOPE = ('https://www.googleapis.com/auth/devstorage.full_control',
             'https://www.googleapis.com/auth/devstorage.read_only',
             'https://www.googleapis.com/auth/devstorage.read_write')

        self.credentials = auth.credentials.with_scopes_if_required(credentials, SCOPE)

        self._refresh_status_codes = refresh_status_codes
        self._max_refresh_attempts = max_refresh_attempts
        self._refresh_timeout = refresh_timeout

        auth_request_session = requests.Session()

        auth_adapter = requests.adapters.HTTPAdapter(max_retries=3)
        auth_request_session.mount("https://", auth_adapter)

        self._auth_request = transport.requests.Request(auth_request_session)
        self._request_session = self._create_request_session(max_retries, pool_block, pool_size)

    def request(self, method, url, data=None, headers=None, **kwargs):
        _credential_refresh_attempt = kwargs.pop(
            '_credential_refresh_attempt', 0)

        request_headers = headers.copy() if headers is not None else {}

        self.credentials.before_request(
            self._auth_request, method, url, request_headers)

        response = self._request_session.request(
            method, url, data=data, headers=request_headers, **kwargs)

        if (response.status_code in self._refresh_status_codes
                and _credential_refresh_attempt < self._max_refresh_attempts):
        
            auth_request_with_timeout = functools.partial(
                self._auth_request, timeout=self._refresh_timeout)
            self.credentials.refresh(auth_request_with_timeout)

            return self.request(
                method, url, data=data, headers=headers,
                _credential_refresh_attempt=_credential_refresh_attempt + 1,
                **kwargs)

        return response

    def _create_request_session(self, max_retries, pool_block, pool_size):
        request_adapter = requests.adapters.HTTPAdapter(
            max_retries=max_retries,
            pool_block=pool_block,
            pool_connections=pool_size,
            pool_maxsize=pool_size
        )

        request_adapter_https = requests.adapters.HTTPAdapter(
            max_retries=max_retries,
            pool_block=pool_block,
            pool_connections=pool_size,
            pool_maxsize=pool_size
        )

        request_session = requests.Session()

        request_session.mount("http://", request_adapter)
        request_session.mount("https://", request_adapter_https)

        return request_session