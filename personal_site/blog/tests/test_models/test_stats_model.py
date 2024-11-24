from django.test import TestCase
from blog.models import BlogPost, Category, BlogUser, HistoryLog, Stats

class TestStatsModel(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create_user(email="test@test.test", password="testpassword")
        self.category = Category.objects.create(name="test category")
        self.blog_post = BlogPost.objects.create(title="test title", content="test content", author=self.user, category=self.category)
    
    def test_stats_create(self):
        blog_post = BlogPost.objects.get(title="test title")

        self.assertIsNotNone(blog_post.stats)
        self.assertEqual(blog_post.stats.views, 0)
        self.assertEqual(blog_post.stats.likes, 0)
        self.assertEqual(blog_post.stats.dislikes, 0)        
        self.assertEqual(blog_post.stats.visited, {'sessions': []})
        self.assertEqual(blog_post.stats.voted, {'sessions': []})
    
    def test_stats_update(self):
        blog_post = BlogPost.objects.get(title="test title")

        blog_post.stats.views += 1
        blog_post.stats.likes += 1
        blog_post.stats.dislikes += 1
        blog_post.stats.visited['sessions'].append('test_session')
        blog_post.stats.voted['sessions'].append('test_session')
        blog_post.stats.save()
        
        updated_stats = BlogPost.objects.get(title="test title").stats

        self.assertEqual(updated_stats.views, 1)
        self.assertEqual(updated_stats.likes, 1)
        self.assertEqual(updated_stats.dislikes, 1)
        self.assertEqual(updated_stats.visited, {'sessions': ['test_session']})
        self.assertEqual(updated_stats.voted, {'sessions': ['test_session']})
    
    def test_stats_delete(self):
        blog_post = BlogPost.objects.get(title="test title")
        stats = blog_post.stats

        blog_post.stats.delete()

        self.assertIsNone(Stats.objects.filter(id=stats.id).first())
        self.assertEqual(len(BlogPost.objects.filter(title="test title")), 0)
