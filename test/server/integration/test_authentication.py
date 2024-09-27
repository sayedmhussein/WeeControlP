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

    def test_two_sessions(self):
        response = self.client.head(path)
        assert response.is_client_error

        # First Login
        self.client.headers["User-Agent"] = "Test 1"
        self.client.cookies.clear()
        response = self.authenticate()
        cookie1 = self.client.cookies.get("token")
        assert response.is_success
        response = self.client.head(path)
        assert response.is_success

        # Second Login
        self.client.headers["User-Agent"] = "Test 2"
        self.client.cookies.clear()
        response = self.authenticate()
        cookie2 = self.client.cookies.get("token")
        assert response.is_success
        response = self.client.head(path)
        assert response.is_success

        # Terminate First With Wrong Device
        self.client.headers["User-Agent"] = "Test 2"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie1
        response = self.client.delete(path)
        assert response.is_client_error

        # First Still Active
        self.client.headers["User-Agent"] = "Test 1"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie1
        response = self.client.head(path)
        assert response.is_success

        # Terminate First With Correct Device
        self.client.headers["User-Agent"] = "Test 1"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie1
        response = self.client.delete(path)
        assert response.is_success

        # Is First Terminated
        self.client.headers["User-Agent"] = "Test 1"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie1
        response = self.client.head(path)
        print("Bla is: ", response.text)
        assert response.is_client_error

        # Second Not Terminated
        self.client.headers["User-Agent"] = "Test 2"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie2
        response = self.client.head(path)
        assert response.is_success

        # Terminate Second With Correct Device
        self.client.headers["User-Agent"] = "Test 2"
        self.client.cookies.clear()
        self.client.cookies["token"] = cookie2
        response = self.client.delete(path)
        assert response.is_success

    def test_change_device(self):
        self.client.headers["Device"] = "Test 1"
        response = self.authenticate()
        assert response.cookies.get("token") is not None

        response = self.client.head(path)
        assert response.is_success

        self.client.headers["Device"] = "Test 2"
        response = self.client.head(path)
        assert response.is_client_error

        self.client.headers["Device"] = "Test 1"
        response = self.client.head(path)
        assert response.is_success

if __name__ == '__main__':
    unittest.main()
