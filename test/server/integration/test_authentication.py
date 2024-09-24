import unittest

from server.routes import V2_USER_AUTHENTICATION
from test.server.integration.test_base import BaseTestCase, encode

path = V2_USER_AUTHENTICATION

class AuthenticationTestCase(BaseTestCase):
    def test_valid_login(self):
        response = self.client.delete(path)
        assert response.is_client_error

        response = self.authenticate()
        assert response.is_success

        response = self.client.delete(path)
        assert response.is_success

        response = self.client.delete(path)
        assert response.is_client_error


    def test_invalid_user(self):
        with self.subTest():
            content = encode(dict(username="notfound", password="password"))
            response = self.client.post(path, content=content)
            assert response.is_success == False

        with self.subTest():
            content = encode(dict(username="username", password="wrong password"))
            response = self.client.post(path, content=content)
            assert response.is_success == False

if __name__ == '__main__':
    unittest.main()
