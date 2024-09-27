import unittest

from server.services.authorization import claims_approved


class MyTestCase(unittest.TestCase):
    def test_when_claims_exist(self):
        self.assertTrue(claims_approved({}, {}))
        self.assertTrue(claims_approved(dict(), dict()))
        self.assertTrue(claims_approved({}, dict(claim="value", claim2="")))
        self.assertTrue(claims_approved({}, {"claim": "value"}))
        self.assertTrue(claims_approved(dict(claim=""), dict(claim="")))
        self.assertTrue(claims_approved(dict(claim=""), dict(claim="value")))
        self.assertTrue(claims_approved(dict(claim="value"), dict(claim="value")))
        self.assertTrue(claims_approved(dict(claim="  value"), dict(claim="value  ")))
        self.assertTrue(claims_approved({"claim": "value1||value2"}, {"claim": "value2"}))
        self.assertTrue(claims_approved({"claim": "value1|| value2"}, {"claim": "value2"}))
        self.assertTrue(claims_approved({"claim": "value1 || value2"}, {"claim": "value2"}))
        self.assertTrue(claims_approved(dict(claim="value1"), dict(claim="value1", claim2="value2")))
        self.assertTrue(claims_approved({"claim1": "value1", "claim2": ""}, dict(claim1="value1", claim2="")))

        self.assertFalse(claims_approved({"claim": ""}, {}))
        self.assertFalse(claims_approved({"claim": "value"}, {}))
        self.assertFalse(claims_approved({"claim": "value"}, {"claim": "not value"}))
        self.assertFalse(claims_approved({"claim": "value"}, {"not claim": "value"}))
        self.assertFalse(claims_approved({"claim": "value1&&value2"}, {"claim": "value2"}))
        self.assertFalse(claims_approved({"claim": "value1||value2"}, {"claim": "value3"}))



if __name__ == '__main__':
    unittest.main()
