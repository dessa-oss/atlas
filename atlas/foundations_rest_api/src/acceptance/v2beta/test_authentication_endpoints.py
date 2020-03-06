
from foundations_spec import Spec


class TestAuthenticationEndpoints(Spec):
    URL = '/api/v2beta/auth/{action}'

    def client(self):
        from foundations_rest_api.global_state import app_manager
        return app_manager.app().test_client()

    def _basic_auth(self):
        import base64
        password = 'test'
        username = 'test'
        return base64.b64encode(f'{username}:{password}'.encode()).decode()

    def _auth_request(self):
        return self.client().get(self.URL.format(action='cli_login'), headers={
            'Authorization': f'Basic {self._basic_auth()}'
        })

    def test_cli_login(self):
        res = self._auth_request()
        self.assertEqual(200, res.status_code)

    def test_logout(self):
        login_res = self._auth_request()
        refresh_token = login_res.json['refresh_token']

        logout_res = self.client().get(self.URL.format(action='logout'), headers={
            'Authorization': f'Bearer {refresh_token}'
        })
        self.assertEqual(200, logout_res.status_code)
