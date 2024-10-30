from django.urls import path
from . import views

app_name = 'matchmaking'

urlpatterns = [
    path('recherche/', views.recherche_match, name='recherche_match'),
    path('resultats/', views.resultats, name='resultats'),
]
