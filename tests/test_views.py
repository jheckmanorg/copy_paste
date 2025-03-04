from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from pastes.models import Paste

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.paste = Paste.objects.create(
            user=self.user,
            content='Test content',
            expires_at=timezone.now() + timedelta(minutes=30)
        )

    def test_signup_get(self):
        """Test GET request to signup page"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post_success(self):
        """Test successful user registration"""
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_post_password_mismatch(self):
        """Test signup with mismatched passwords"""
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'different'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b"The two password fields didn\xe2\x80\x99t match.")

    def test_signup_post_short_password(self):
        """Test signup with too short password"""
        data = {
            'username': 'newuser',
            'password1': 'short',
            'password2': 'short'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short.")

    def test_signup_post_missing_fields(self):
        """Test signup with missing fields"""
        data = {
            'username': '',
            'password1': '',
            'password2': ''
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")

    def test_signup_post_existing_username(self):
        """Test signup with already existing username"""
        # First create a user
        User.objects.create_user(username='existinguser', password='testpass123')
        
        # Try to create another user with the same username
        data = {
            'username': 'existinguser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.")

    def test_paste_list_authenticated(self):
        """Test paste list view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('paste_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pastes/list.html')
        self.assertIn('pastes', response.context)
        self.assertEqual(list(response.context['pastes']), [self.paste])

    def test_paste_list_unauthenticated(self):
        """Test paste list view redirects for unauthenticated user"""
        response = self.client.get(reverse('paste_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/')

    def test_create_paste_get(self):
        """Test GET request to create paste page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('create_paste'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pastes/create.html')

    def test_create_paste_post(self):
        """Test creating a new paste"""
        self.client.login(username='testuser', password='testpass123')
        data = {'content': 'New paste content'}
        response = self.client.post(reverse('create_paste'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Paste.objects.filter(content='New paste content').exists())

    def test_extend_paste_success(self):
        """Test successful paste extension"""
        self.client.login(username='testuser', password='testpass123')
        initial_expiry = self.paste.expires_at
        response = self.client.post(reverse('extend_paste', args=[self.paste.id]))
        self.assertEqual(response.status_code, 302)
        self.paste.refresh_from_db()
        self.assertTrue(self.paste.expires_at > initial_expiry)

    def test_extend_paste_too_far_future(self):
        """Test paste extension when expiry is too far in future"""
        self.client.login(username='testuser', password='testpass123')
        # Set expiry to more than 1 hour in future
        future_time = timezone.now() + timedelta(hours=2)
        self.paste.expires_at = future_time
        self.paste.save()
        
        response = self.client.post(reverse('extend_paste', args=[self.paste.id]))
        self.assertEqual(response.status_code, 302)
        self.paste.refresh_from_db()
        # Expiry should not have changed
        self.assertAlmostEqual(
            self.paste.expires_at.timestamp(),
            future_time.timestamp(),
            delta=1  # Allow 1 second difference due to processing time
        )

    def test_extend_paste_unauthenticated(self):
        """Test paste extension redirects for unauthenticated user"""
        response = self.client.post(reverse('extend_paste', args=[self.paste.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next=/extend/{self.paste.id}/')

    def test_extend_paste_wrong_user(self):
        """Test that users cannot extend pastes they don't own"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123'
        )
        self.client.login(username='otheruser', password='testpass123')
        
        # Try to extend paste owned by self.user
        response = self.client.post(reverse('extend_paste', args=[self.paste.id]))
        self.assertEqual(response.status_code, 403)  # Should return Forbidden
        
        # Verify expiry time didn't change
        self.paste.refresh_from_db()
        self.assertEqual(
            self.paste.expires_at.timestamp(),
            self.paste.expires_at.timestamp()
        )
