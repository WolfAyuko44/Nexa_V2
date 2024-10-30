from django import forms
from .models import MatchmakingRequest, ProfilUtilisateur

class MatchmakingRequestForm(forms.ModelForm):
    class Meta:
        model = MatchmakingRequest
        fields = ['niveau_recherche', 'style_jeu_recherche', 'region_recherche', 'langue_recherche']
        widgets = {
            'niveau_recherche': forms.NumberInput(attrs={'min': 1}),
            'style_jeu_recherche': forms.Select(choices=ProfilUtilisateur._meta.get_field('style_jeu').choices),
            'region_recherche': forms.Select(choices=ProfilUtilisateur._meta.get_field('region').choices),
            'langue_recherche': forms.Select(choices=ProfilUtilisateur._meta.get_field('langue').choices),
        }
