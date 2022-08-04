import unittest
from app.models import User


class UserModelTest(unittest.TestCase):

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_match(self):
        u = User(password='cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))
