from django.shortcuts import render, redirect, get_object_or_404
from .models import Comment, Like
from django.contrib.auth.decorators import login_required
from apps.utilisateurs.models import Post

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(post=post, utilisateur=request.user, texte=text)
    return redirect('partage_contenu:post_detail', post_id=post.id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    utilisateur = request.user

    # Vérifie si le like existe déjà
    like, created = Like.objects.get_or_create(utilisateur=utilisateur, post=post)

    if not created:
        # Si le like existe déjà, le supprimer
        like.delete()
    
    return redirect('partage_contenu:post_detail', post_id=post_id) 

@login_required
def home(request):
    # Récupérer tous les posts
    posts = Post.objects.all().order_by('-created_at')

    # Ajout de la vérification des likes pour chaque post
    for post in posts:
        post.total_likes_count = post.total_likes()  # Compte le nombre de likes
        post.user_liked = post.liked_by_user(request.user)  # Vérifie si l'utilisateur a aimé le post

    return render(request, 'partage_contenu/home.html', {'posts': posts})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Récupère tous les commentaires pour le post
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'partage_contenu/post_detail.html', context)
