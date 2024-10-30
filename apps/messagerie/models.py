# apps/messagerie/models.py

from django.conf import settings
from django.db import models

class Conversation(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name='Participants'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='Envoyeur'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversation'
    )
    content = models.TextField(verbose_name='Contenu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')

    def __str__(self):
        return f"Message {self.id} from {self.sender}"
