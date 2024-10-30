from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Avantage(models.Model):
    """
    Modèle pour les avantages associés à chaque type d'abonnement.
    """
    nom = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.nom

class TypeAbonnement(models.Model):
    """
    Modèle pour définir les types d'abonnement.
    """
    nom = models.CharField(max_length=50, unique=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree_jours = models.PositiveIntegerField(default=30)  
    avantages = models.ManyToManyField(Avantage, related_name='abonnements', blank=True)

    def __str__(self):
        return self.nom

class Abonnement(models.Model):
    """
    Modèle principal pour l'abonnement d'un utilisateur.
    """
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='abonnements')
    type_abonnement = models.ForeignKey(TypeAbonnement, on_delete=models.CASCADE)
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField()
    badge_abonnement = models.BooleanField(default=False)
    renouvellement_auto = models.BooleanField(default=True)
    mode_paiement = models.CharField(max_length=100, blank=True, null=True)
    statut = models.CharField(max_length=20, default='actif')  # actif, expiré, suspendu

    def __str__(self):
        return f'{self.utilisateur.username} - {self.type_abonnement.nom}'

    def est_active(self):
        return self.date_fin > timezone.now()

    def activer_badge(self):
        """Active le badge si l'abonnement est Premium."""
        self.badge_abonnement = True if self.type_abonnement.nom == 'Premium' else False

    def sauvegarder_dans_base(self):
        """Sauvegarde l'abonnement et active le badge si nécessaire."""
        self.activer_badge()
        self.save()

    def renouveler(self):
        """Renouvelle l'abonnement si le renouvellement automatique est activé."""
        if self.renouvellement_auto and self.est_active():
            self.date_debut = timezone.now()
            self.date_fin = timezone.now() + timedelta(days=self.type_abonnement.duree_jours)
            self.save()

    def envoyer_notification_expiration(self):
        """Envoie une notification si l'abonnement est sur le point d'expirer."""
        if self.date_fin - timezone.now() < timedelta(days=7):
            # Logique d'envoi de notification
            pass

    class Meta:
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
        ordering = ['-date_debut']

class Paiement(models.Model):
    """
    Modèle pour suivre les paiements effectués pour les abonnements.
    """
    abonnement = models.ForeignKey(Abonnement, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, default='complété')  # complété, en attente, échoué

    def __str__(self):
        return f'Paiement {self.id} pour {self.abonnement.utilisateur.username} - {self.montant}'

