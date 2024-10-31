from django.urls import path
from . import views

app_name = 'recherche'

urlpatterns = [
    path('', views.recherche_utilisateur, name='recherche_utilisateur'),
]
