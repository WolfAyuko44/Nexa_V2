from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.notifications_messagerie.models import Notification

class NotificationTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.sender = User.objects.create_user(username='sender', password='password')
        self.recipient = User.objects.create_user(username='recipient', password='password')
        self.notification = Notification.objects.create(
            message='Test Notification',
            recipient=self.recipient,
            sender=self.sender
        )

    def test_notification_creation(self):
        """Test si la notification est correctement créée."""
        self.assertEqual(self.notification.message, 'Test Notification')
        self.assertEqual(self.notification.recipient, self.recipient)
        self.assertFalse(self.notification.is_read)

    def test_mark_as_read(self):
        """Test si la notification peut être marquée comme lue."""
        self.notification.is_read = True
        self.notification.save()
        self.assertTrue(self.notification.is_read)

    def test_unread_count(self):
        """Test du nombre de notifications non lues."""
        self.assertEqual(self.recipient.notifications.filter(is_read=False).count(), 1)
