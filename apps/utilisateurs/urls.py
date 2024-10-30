from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'utilisateurs'

urlpatterns = [
    path('', views.home, name='home'),
    path('connexion/', views.connexion, name='connexion'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('contact/', views.contact, name='contact'),
    path('profil/<str:username>/', views.profil_detail, name='profil_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('changer-photo-profil/', views.changer_photo_profil, name='changer_photo_profil'),
    path('about/', views.about_view, name='about'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_details, name='post_details'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('search/', views.search_view, name='search'),
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('mot-de-passe-oublie/envoye/', views.mot_de_passe_oublie_envoye, name='mot_de_passe_oublie_envoye'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
