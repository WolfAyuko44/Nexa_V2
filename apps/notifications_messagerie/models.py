from django.db import models
from apps.utilisateurs.models import Utilisateur  # Assurez-vous que le chemin est correct

class Notification(models.Model):
    """
    Modèle représentant une notification.
    """
    MESSAGE_TYPES = (
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('success', 'Succès'),
        ('error', 'Erreur'),
    )

    message = models.CharField(max_length=255)
    recipient = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='sent_notifications')
    priority = models.IntegerField(default=0)  # 0 = Normal, 1 = Élevé, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='info')  # Type de message
    related_url = models.URLField(blank=True, null=True)  # Lien vers la ressource concernée
    context = models.JSONField(blank=True, null=True)  # Stocker des informations supplémentaires sous forme de JSON

    def __str__(self):
        return f'[{self.get_message_type_display()}] {self.message} - {self.recipient.username}'

    class Meta:
        ordering = ['-created_at']  # Trier les notifications par date de création (les plus récentes en premier)
