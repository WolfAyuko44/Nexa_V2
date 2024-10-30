from django import forms
from apps.utilisateurs.models import Utilisateur
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm

class UtilisateurModificationForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'localisation', 'avatar', 'profil_public', 'affichage_statistiques', 'phone_number'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre biographie'}),
            'localisation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre localisation'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'profil_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'affichage_statistiques': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
        }

class PrivacySettingsForm(forms.ModelForm):
    class Meta:
        model = Utilisateur  # Assurez-vous que ce modèle est correct
        fields = ['profil_public']
        widgets = {
            'profil_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SecurityForm(forms.Form):
    old_password = forms.CharField(
        label="Ancien mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ancien mot de passe'})
    )
    new_password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'})
    )
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    )

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'site_web', 'localisation', 'avatar',
            'profil_public', 'affichage_statistiques'
        )
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre biographie'}),
            'site_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'http://votre-site.com'}),
            'localisation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre localisation'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BaseInfoForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Adresse e-mail'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Votre biographie'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'dob', 'gender', 'nationality', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nationalité'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Biographie'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Assurez-vous que tous les champs ont la classe 'form-control'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
