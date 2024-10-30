from django import forms
from .models import Abonnement
from datetime import timedelta
from django.utils import timezone

class AbonnementForm(forms.ModelForm):
    class Meta:
        model = Abonnement
        fields = ['date_fin']
        widgets = {
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }


    def save(self, commit=True):
        """
        Surcharge de la méthode save() pour gérer la date de fin automatiquement.
        La durée de l'abonnement est fixée à un mois (30 jours).
        """
        abonnement = super().save(commit=False)

        # Date de début automatique (maintenant) et fin dans 30 jours
        abonnement.date_debut = timezone.now()
        abonnement.date_fin = abonnement.date_debut + timedelta(days=30)

        if commit:
            abonnement.save()

        return abonnement
