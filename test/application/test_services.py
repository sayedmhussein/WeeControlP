import unittest

from application.services import hash_new_password, is_correct_password


class MyTestCase(unittest.TestCase):
    def test_something(self):
        password = "Thank you https://stackoverflow.com/a/56915300/893857"
        salt, pw_hash = hash_new_password(password)
        self.assertTrue(is_correct_password(salt, pw_hash, password))
        assert not is_correct_password(salt, pw_hash, 'Tr0ub4dor&3')
        assert not is_correct_password(salt, pw_hash, 'rosebud')


if __name__ == '__main__':
    unittest.main()
