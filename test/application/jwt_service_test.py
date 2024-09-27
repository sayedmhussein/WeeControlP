import unittest

from server.services.secuity import get_jwt, get_claims


class GetJwtCase(unittest.TestCase):
    def test_when_no_claims(self):
        token = get_jwt({})
        self.assertTrue(len(token) > 10)
        claims = get_claims(token)
        self.assertTrue(claims is not None)

    def test_when_with_claims(self):
        dictionary = {'key1': 'value1', 'key2': 'value2'}
        token = get_jwt(dictionary)
        self.assertTrue(len(token) > 10)
        claims = get_claims(token)
        self.assertTrue(dictionary.items() <= claims.items())


    def test_standard_claims(self):
        token = get_jwt({})
        claims = get_claims(token)
        self.assertTrue(len(claims) > 0)
        self.assertIn('iat', claims)
        self.assertIn('exp', claims)
        self.assertIn('iss', claims)


if __name__ == '__main__':
    unittest.main()
