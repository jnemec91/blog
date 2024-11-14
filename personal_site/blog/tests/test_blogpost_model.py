from django.test import TestCase
from blog.models import BlogPost, Category, BlogUser, HistoryLog
from blog.utils.hashmaker import make_hash_from_model


class BlogPostModelTest(TestCase):
    def setUp(self):
        self.user = BlogUser.objects.create(email="test@test.test", password="testpassword", first_name="test", last_name="user")
        self.category = Category.objects.create(name="test category")
        self.blog_post = BlogPost.objects.create(title="test title", content="test content", author=self.user, category=self.category)

    def test_blog_post_create(self):
        # get the blog post
        blog_post = BlogPost.objects.get(title="test title")

        # assertions
        self.assertEqual(blog_post.title, "test title")
        self.assertEqual(blog_post.content, "test content")
        self.assertEqual(blog_post.author, self.user)
        self.assertEqual(blog_post.category, self.category)

        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Blog created")
        self.assertEqual(HistoryLog.objects.last().source, f"None:{blog_post}")
    
    def test_blog_post_update(self):
        # get the blog post
        blog_post = BlogPost.objects.get(title="test title")

        # update the blog post
        blog_post.title = "updated title"
        blog_post.content = "updated content"
        blog_post.save()

        # get the updated blog post
        BlogPost.objects.get(id=blog_post.pk)

        # assertions
        self.assertEqual(blog_post.title, "updated title")
        self.assertEqual(blog_post.content, "updated content")
        self.assertEqual(blog_post.author, self.user)
        self.assertEqual(blog_post.category, self.category)
        
        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Blog updated")
        self.assertEqual(HistoryLog.objects.last().source, f"{blog_post.pk}:{blog_post}")
    
    def test_blog_post_delete(self):
        # get the blog post
        blog_post = BlogPost.objects.get(title="test title")
        id = blog_post.pk

        # delete the blog post
        blog_post.delete()

        # assertions
        self.assertEqual(BlogPost.objects.count(), 0)

        # assert history log message was created
        self.assertEqual(HistoryLog.objects.last().action, "Blog deleted")
        self.assertEqual(HistoryLog.objects.last().source, f"{id}:{blog_post}")
    
    def test_blog_post_str(self):
        # get the blog post
        blog_post = BlogPost.objects.get(title="test title")

        # assertions
        self.assertEqual(str(blog_post), "BlogPost: test title")
    
    def test_blog_post_hash_field(self):
        # get the blog post
        blog_post = BlogPost.objects.get(title="test title")

        # assertions
        self.assertEqual(len(blog_post.hash_field), 32)
        self.assertEqual(blog_post.hash_field, make_hash_from_model(blog_post))
