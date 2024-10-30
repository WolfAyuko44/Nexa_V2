from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['nom', 'description', 'prix', 'categorie', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'prix': forms.NumberInput(attrs={'step': 0.01}),
        }

class ArticleFilterForm(forms.Form):
    CATEGORIES = Article.CATEGORIES
    categorie = forms.ChoiceField(choices=[('', 'Toutes les catégories')] + CATEGORIES, required=False)
