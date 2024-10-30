from django import forms
from .models import Contenu, Commentaire

class ContenuForm(forms.ModelForm):
    class Meta:
        model = Contenu
        fields = ['titre', 'description', 'fichier', 'type_contenu']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['texte']
        widgets = {
            'texte': forms.Textarea(attrs={'rows': 3}),
        }
