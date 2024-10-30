from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (UtilisateurCreationForm, UtilisateurModificationForm,
                    ConnexionForm, ProfilePictureForm, SignUpForm,
                    PostForm, MotDePasseOublieForm)
from .models import Utilisateur, Post
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def signup(request):
    """Vue pour l'inscription des utilisateurs."""
    if request.user.is_authenticated:
        messages.info(request, "Vous êtes déjà connecté.")
        return redirect('home')

    form = SignUpForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            try:
                user = form.save()
                # Connexion de l'utilisateur après l'inscription
                login(request, user)
                messages.success(request, f"Inscription réussie ! Bienvenue, {user.username}.")
                return redirect('home')  # Redirection vers la page d'accueil
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription : {str(e)}")
        else:
            messages.warning(request, "Veuillez corriger les erreurs du formulaire.")

    return render(request, 'utilisateurs/signup.html', {'form': form})

def connexion(request):
    """Vue pour la connexion des utilisateurs."""
    form = ConnexionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Connexion réussie !')
            return redirect('utilisateurs:home')  # Assurez-vous que ce chemin est correct
        else:
            form.add_error(None, 'Identifiant ou mot de passe incorrect.')

    return render(request, 'utilisateurs/login.html', {'form': form})

@login_required
def profile_view(request):
    """Vue pour afficher le profil de l'utilisateur connecté."""
    utilisateur = request.user
    return render(request, 'utilisateurs/profil.html', {'utilisateur': utilisateur})

@login_required
def changer_photo_profil(request):
    """Vue pour changer la photo de profil de l'utilisateur connecté."""
    form = ProfilePictureForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Photo de profil mise à jour avec succès.')
        return redirect('utilisateurs:profil')

    return render(request, 'utilisateurs/profile_picture.html', {'form': form})

@login_required
def profil_detail(request, username):
    """Vue pour afficher les détails du profil d'un utilisateur spécifique."""
    utilisateur = get_object_or_404(Utilisateur, username=username)
    return render(request, 'utilisateurs/profil.html', {'utilisateur': utilisateur})

class MotDePasseOublieView(PasswordResetView):
    """Vue pour la réinitialisation du mot de passe oublié."""
    template_name = 'utilisateurs/mot_de_passe_oublie.html'
    email_template_name = 'utilisateurs/email/mot_de_passe_oublie_email.html'
    subject_template_name = 'utilisateurs/email/mot_de_passe_oublie_subject.txt'
    success_url = '/mot-de-passe-oublié/envoye/'

def mot_de_passe_oublie(request):
    """Vue pour afficher le formulaire de mot de passe oublié."""
    form = MotDePasseOublieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        messages.success(request, 'Un email de réinitialisation du mot de passe a été envoyé si l\'adresse est enregistrée.')
        return redirect('mot_de_passe_oublie_envoye')

    return render(request, 'utilisateurs/mot_de_passe_oublie.html', {'form': form})

def mot_de_passe_oublie_envoye(request):
    """Vue pour afficher un message de confirmation après l'envoi du mot de passe oublié."""
    return render(request, 'utilisateurs/mot_de_passe_oublie_envoye.html')

def home(request):
    """Vue pour la page d'accueil."""
    return render(request, 'utilisateurs/index.html')

def search_view(request):
    """Vue pour afficher les résultats de recherche."""
    return render(request, 'search_results.html', {})

def privacy_policy(request):
    """Vue pour afficher la politique de confidentialité."""
    return render(request, 'utilisateurs/privacy_policy.html')

def terms_of_service(request):
    """Vue pour afficher les conditions de service."""
    return render(request, 'utilisateurs/terms_of_service.html')

def contact(request):
    """Vue pour afficher la page de contact."""
    return render(request, 'utilisateurs/contact.html')

def signup_view(request):
    """Vue pour afficher la page d'inscription."""
    return render(request, 'signup.html')

def about_view(request):
    """Vue pour afficher la page À Propos."""
    return render(request, 'utilisateurs/about.html', {'page_title': 'À Propos'})

@login_required
def create_post(request):
    """Vue pour créer un nouveau post."""
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.utilisateur = request.user
        post.save()
        messages.success(request, 'Post créé avec succès.')
        return redirect('utilisateurs:profil_detail', username=request.user.username)

    return render(request, 'utilisateurs/create_post.html', {'form': form})

def post_details(request, post_id):
    """Vue pour afficher les détails d'un post spécifique."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Si tu as un modèle de commentaire
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'utilisateurs/post_details.html', context)

@login_required
def post_delete(request, post_id):
    """Vue pour supprimer un post."""
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, 'Post supprimé avec succès.')
    return redirect('utilisateurs:profil_detail', username=request.user.username)

# Ajouter une vue protégée en exemple
@login_required
def protected_view(request):
    """Vue protégée accessible uniquement aux utilisateurs connectés."""
    return render(request, 'utilisateurs/protected_view.html')
