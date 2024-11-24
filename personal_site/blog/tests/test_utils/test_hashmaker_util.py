from django.test import TestCase
from blog.utils.hashmaker import make_32_bit_hash, make_hash_from_model
from blog.models import BlogUser, Category, BlogPost


class TestHashmakerUtil(TestCase):
    def test_make_32_bit_hash(self):
        pk = 1
        string = 'test'
        self.assertEqual(make_32_bit_hash(pk, string), 'ba88c155ba898fc8b5099893036ef205')

        pk = 2
        string = 'test'
        self.assertEqual(make_32_bit_hash(pk, string), '7cbab5cea99169139e7e6d8ff74ebb77')

        pk = 1
        string = 'test2'
        self.assertEqual(make_32_bit_hash(pk, string), '6c58ecf636ac0ebfdb3cc7b1ceabd42b')
    
    def test_make_hash_from_model(self):
        user = BlogUser.objects.create_user(email="test@test.test", password="test")
        self.assertEqual(make_hash_from_model(user), '42ca2ecf0492a53883f851489ab164b8')

        category = Category.objects.create(name="test")
        self.assertEqual(make_hash_from_model(category), 'b87b33c48f7c99b5c217311df458de9b')
    
        blog_post = BlogPost.objects.create(title="test", content="test", author=user, category=category)
        self.assertEqual(make_hash_from_model(blog_post), '7e8ef2b524b3ecd6fd97f581284e7b79')