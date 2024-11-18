from blog.forms.LoginForm import LoginForm
from django.test import TestCase, RequestFactory
from blog.models import BlogUser
from django.contrib.sessions.middleware import SessionMiddleware

class TestLoginForm(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = BlogUser.objects.create_user(email='test@test.test', password='password')

    def test_login(self):
        request = self.factory.post('/login/', {'email': 'test@test.test', 'password': 'password'})
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        form = LoginForm(request.POST)

        self.assertTrue(form.is_valid(request))
        self.assertEqual(form.login(request), self.user)

    def test_invalid_login(self):
        request = self.factory.post('/login/', {'email': 'random@random.test', 'password': 'random'})
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()        
        form = LoginForm(request.POST)

        self.assertFalse(form.is_valid(request))
        self.assertIsNone(form.login(request))

    def test_missing_email(self):
        request = self.factory.post('/login/', {'password': 'password'})
        form = LoginForm(request.POST)

        self.assertFalse(form.is_valid(request))
        self.assertIsNone(form.login(request))
    
    def test_missing_password(self):
        request = self.factory.post('/login/', {'email': 'test@test.test'})
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()        
        form = LoginForm(request.POST)

        self.assertFalse(form.is_valid(request))
        self.assertIsNone(form.login(request))