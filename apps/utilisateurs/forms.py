from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Utilisateur, Post
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'site_web', 'localisation')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Une brève biographie...'}),
            'site_web': forms.URLInput(attrs={'placeholder': 'http://votresite.com'}),
            'localisation': forms.TextInput(attrs={'placeholder': 'Votre localisation'}),
        }

class UtilisateurModificationForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'localisation', 'avatar', 'profil_public')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'localisation': forms.TextInput(attrs={'placeholder': 'Votre localisation'}),
            'avatar': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class ConnexionForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Requis. Entrez une adresse email valide.",
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Utilisateur
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d’utilisateur'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class MotDePasseOublieForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Votre email'}))

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('avatar',)
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'multiple': False}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Décrivez votre post...'}),
            'image': forms.ClearableFileInput(attrs={'multiple': False}),
        }
