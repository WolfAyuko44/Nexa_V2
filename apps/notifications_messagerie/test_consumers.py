# apps/notifications_messagerie/test_consumers.py

import json
from channels.testing import WebsocketCommunicator
from channels.testing import ChannelsLiveServerTestCase
from apps.notifications_messagerie.consumers import NotificationConsumer
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumerTests(ChannelsLiveServerTestCase):
    
    async def asyncSetUp(self):
        # Importez les modèles ici
        from apps.notifications_messagerie.models import Notification

        # Créez des utilisateurs pour le test
        self.sender = await User.objects.create_user(username='sender', password='password')
        self.recipient = await User.objects.create_user(username='recipient', password='password')
        
        # Configurez le WebSocket Communicator
        self.communicator = WebsocketCommunicator(NotificationConsumer.as_asgi(), f"ws://localhost/notifications/")
        
        # Accepter la connexion
        self.connected, _ = await self.communicator.connect()

    async def asyncTearDown(self):
        # Fermez le WebSocket après le test
        await self.communicator.disconnect()

    async def test_send_notification(self):
        # Simulez l'envoi d'une notification
        notification_data = {
            'message': 'Hello from the sender!',
            'recipient': self.recipient.id
        }
        
        # Envoyez la notification
        await self.communicator.send_json(notification_data)
        
        # Recevez le message
        response = await self.communicator.receive_json()
        
        # Vérifiez que le message reçu est correct
        self.assertEqual(response['message'], notification_data['message'])

    async def test_receive_notification(self):
        # Simulez l'envoi d'une notification pour un autre utilisateur
        notification_data = {
            'message': 'New message for you!',
            'recipient': self.recipient.id
        }
        
        # Envoyez la notification
        await self.communicator.send_json(notification_data)

        # Recevez le message
        response = await self.communicator.receive_json()

        # Vérifiez que le message reçu est correct
        self.assertEqual(response['message'], notification_data['message'])
