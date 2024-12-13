from django.test import TestCase
from django.contrib.auth import get_user_model

class TestUserManagers(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            password='testpassword', email='test@test.test', first_name='test', last_name='user'
        )

        self.assertEqual(user.email, 'test@test.test')
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # none username should be created
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpassword')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            password='testpassword', email='test@test.test', first_name='test', last_name='user'
        )

        self.assertEqual(admin_user.email, 'test@test.test')
        self.assertEqual(admin_user.first_name, 'test')
        self.assertEqual(admin_user.last_name, 'user')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        # none username should be created
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)

