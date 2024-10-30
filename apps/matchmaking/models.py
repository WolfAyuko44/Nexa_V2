from django.db import models
from django.contrib.auth.models import User
from config import settings

class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    niveau = models.IntegerField(default=1)
    style_jeu = models.CharField(max_length=100, choices=[('Offensif', 'Offensif'), ('Défensif', 'Défensif'), ('Équilibré', 'Équilibré')], default='Équilibré')
    region = models.CharField(max_length=100, choices=[('Europe', 'Europe'), ('Amérique du Nord', 'Amérique du Nord'), ('Asie', 'Asie')], default='Europe')
    langue = models.CharField(max_length=100, choices=[('Français', 'Français'), ('Anglais', 'Anglais'), ('Espagnol', 'Espagnol')], default='Français')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.niveau}"

class MatchmakingRequest(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    niveau_recherche = models.IntegerField(default=1)
    style_jeu_recherche = models.CharField(max_length=100, choices=[('Offensif', 'Offensif'), ('Défensif', 'Défensif'), ('Équilibré', 'Équilibré')], default='Équilibré')
    region_recherche = models.CharField(max_length=100, choices=[('Europe', 'Europe'), ('Amérique du Nord', 'Amérique du Nord'), ('Asie', 'Asie')], default='Europe')
    langue_recherche = models.CharField(max_length=100, choices=[('Français', 'Français'), ('Anglais', 'Anglais'), ('Espagnol', 'Espagnol')], default='Français')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Demande de {self.utilisateur.username} - {self.niveau_recherche} {self.style_jeu_recherche}"
    
    class Meta:
        ordering = ['date_creation']
