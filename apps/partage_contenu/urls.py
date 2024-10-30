from django.urls import path
from . import views
from apps.partage_contenu.views import like_post

app_name = 'partage_contenu'

urlpatterns = [
    # Page d'accueil qui affiche tous les posts pour les utilisateurs connectés
    path('', views.home, name='home'),
    
    # URL pour afficher les détails d'un post spécifique
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # URL pour ajouter un commentaire à un post spécifique
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # URL pour aimer ou désaimer un post spécifique
    path('post/<int:post_id>/like/', like_post, name='like_post'),
]
