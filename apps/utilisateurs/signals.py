from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Utilisateur

@receiver(post_save, sender=Utilisateur)
def utilisateur_post_save(sender, instance, created, **kwargs):
    if created:
        # Action à exécuter lorsqu'un nouvel utilisateur est créé
        print(f'Nouvel utilisateur créé : {instance.username}')
        # Envoi d'un email de bienvenue
        send_mail(
            'Bienvenue sur Nexa',
            f'Bonjour {instance.username},\n\nMerci de vous être inscrit sur Nexa !\n\nCordialement,\nL’équipe Nexa.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )
    else:
        # Action à exécuter lorsqu'un utilisateur existant est mis à jour
        print(f'Utilisateur mis à jour : {instance.username}')

        # Exemple d'action : log des modifications ou envoyer un message
        # Vous pourriez envisager de sauvegarder un log ou notifier un administrateur
        # logger.info(f'Utilisateur {instance.username} a été mis à jour.')
