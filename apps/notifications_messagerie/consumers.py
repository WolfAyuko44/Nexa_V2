import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        recipient_id = data['recipient_id']
        
        # Envoie le message à tous les clients connectés
        await self.send(text_data=json.dumps({
            'message': message,
            'created_at': str(self.channel_name)  # Remplacez par votre timestamp
        }))
        
        # Vous pouvez également ajouter la logique pour enregistrer la notification dans la base de données ici
