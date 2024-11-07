# apps/recherche/urls.py
from django.urls import path
from . import views

app_name = 'recherche'  # Définit le namespace "recherche"

urlpatterns = [
    path('', views.recherche_utilisateur, name='recherche_utilisateur'),
]
