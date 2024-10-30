# apps/notifications_messagerie/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def create_notification(message, recipient, sender):
    """Crée une nouvelle notification et émet une alerte via WebSocket."""
    notification = Notification.objects.create(
        message=message,
        recipient=recipient,
        sender=sender,
    )
    
    # Émet la notification via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "notify_user",
            "message": notification.message,
            "created_at": notification.created_at.isoformat(),
        }
    )
