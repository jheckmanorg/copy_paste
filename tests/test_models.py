from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from pastes.models import Paste

class PasteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.paste = Paste.objects.create(
            user=self.user,
            content='Test content',
            expires_at=timezone.now() + timedelta(minutes=30)
        )

    def test_paste_creation(self):
        """Test paste instance creation"""
        self.assertTrue(isinstance(self.paste, Paste))
        self.assertEqual(self.paste.content, 'Test content')
        self.assertEqual(self.paste.user, self.user)

    def test_paste_str_representation(self):
        """Test the string representation of a paste"""
        expected = f"Paste by {self.user.username} (expires {self.paste.expires_at})"
        self.assertEqual(str(self.paste), expected)

    def test_paste_auto_created_at(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.paste.created_at)
        self.assertTrue(isinstance(self.paste.created_at, timezone.datetime))

    def test_paste_cascade_delete(self):
        """Test that pastes are deleted when user is deleted"""
        paste_id = self.paste.id
        self.user.delete()
        self.assertFalse(Paste.objects.filter(id=paste_id).exists())
