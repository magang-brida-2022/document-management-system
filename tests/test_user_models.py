import unittest
from app.models import AnonymousUser, Permission, User, Role


class UserModelTest(unittest.TestCase):

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_match(self):
        u = User(password='cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email="john@example.com", username="john", password="dog")
        self.assertTrue(u.can(Permission.TTD))
        self.assertTrue(u.can(Permission.SURAT_KELUAR))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.SURAT_MASUK))
