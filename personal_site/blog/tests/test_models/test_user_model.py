from django.test import TestCase
from django .contrib.auth import get_user_model
from blog.models import BlogUser, HistoryLog
from blog.utils.hashmaker import make_hash_from_model

class TestUserModel(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(email="new@test.test", password="testpassword", first_name="new", last_name="user")

    def test_user_create(self):
        user = BlogUser.objects.get(email="new@test.test")

        self.assertEqual(user.email, "new@test.test")
        self.assertEqual(user.first_name, "new")
        self.assertEqual(user.last_name, "user")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        self.assertEqual(HistoryLog.objects.last().action, "User created")
        self.assertEqual(HistoryLog.objects.last().source, f"NEW:{user}")

    def test_user_update(self):
        user = BlogUser.objects.get(email="new@test.test")

        user.first_name = "updated"
        user.last_name = "updated"
        user.email = "updated@test.test"

        user.set_password("newpassword")
        user.save()

        user = BlogUser.objects.get(id=user.pk)
        
        self.assertEqual(user.email, "updated@test.test")
        self.assertEqual(user.first_name, "updated")
        self.assertEqual(user.last_name, "updated")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # TODO: assert password was updated

    def test_user_delete(self):
        user = BlogUser.objects.get(email="new@test.test")
        id = user.pk
        user.delete()

        self.assertEqual(BlogUser.objects.count(), 0)

        self.assertEqual(HistoryLog.objects.last().action, "User deleted")
        self.assertEqual(HistoryLog.objects.last().source, f"{id}:{user}")
    
    def test_user_str(self):
        user = BlogUser.objects.get(email="new@test.test")

        self.assertEqual(str(user), "User: new@test.test")
    
    def test_user_hash_field(self):
        user = BlogUser.objects.get(email="new@test.test")
        self.assertEqual(len(user.hash_field), 32)
        self.assertEqual(user.hash_field, make_hash_from_model(user))