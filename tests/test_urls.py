from django.test import TestCase
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from pastes import views as paste_views

class UrlsTest(TestCase):
    def test_paste_list_url_resolves(self):
        """Test paste list URL resolution"""
        url = reverse('paste_list')
        self.assertEqual(url, '/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, paste_views.paste_list)

    def test_create_paste_url_resolves(self):
        """Test create paste URL resolution"""
        url = reverse('create_paste')
        self.assertEqual(url, '/create/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, paste_views.create_paste)

    def test_extend_paste_url_resolves(self):
        """Test extend paste URL resolution"""
        url = reverse('extend_paste', args=[1])
        self.assertEqual(url, '/extend/1/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, paste_views.extend_paste)

    def test_login_url_resolves(self):
        """Test login URL resolution"""
        url = reverse('login')
        self.assertEqual(url, '/login/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, auth_views.LoginView)

    def test_logout_url_resolves(self):
        """Test logout URL resolution"""
        url = reverse('logout')
        self.assertEqual(url, '/logout/')
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, auth_views.LogoutView)

    def test_signup_url_resolves(self):
        """Test signup URL resolution"""
        url = reverse('signup')
        self.assertEqual(url, '/signup/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, paste_views.signup)

    def test_invalid_url_returns_404(self):
        """Test that invalid URLs return 404"""
        response = self.client.get('/invalid-url/')
        self.assertEqual(response.status_code, 404)
