import json
import unittest

from starlette.responses import Response
from starlette.testclient import TestClient

from infrastructure.repository import get_db_session
from server.main import get_app
from server.routes import V2_USER_AUTHENTICATION


def encode(text):
    return json.dumps(text).encode()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.db = get_db_session(in_memory=True)
        self.client = TestClient(get_app(self.db))
        self.client.headers["Content-Type"] = "application/json"
        self.client.headers["User-Agent"] = "this is a test case"

    def tearDown(self):
        self.client.headers.clear()
        self.client.cookies.clear()

    def authenticate(self, username="username", password="password"):
        path = V2_USER_AUTHENTICATION
        data = dict(username=username, password=password)

        response = self.client.post(path, content=json.dumps(data).encode())
        token = response.cookies.get("token")
        assert response.status_code == 200
        assert token == response.json()["token"]
        return response

if __name__ == '__main__':
    unittest.main()
