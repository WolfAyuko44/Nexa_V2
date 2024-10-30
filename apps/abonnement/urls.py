from django.urls import path
from . import views
from apps.abonnement.views import modifier_prix_abonnement, create_checkout_session

app_name = 'abonnement'

urlpatterns = [
    path('detail/', views.abonnement_detail, name='abonnement_detail'),
    path('souscrire/', views.souscrire_abonnement, name='souscrire_abonnement'),
    path('modifier/<int:abonnement_id>/', views.modifier_abonnement, name='modifier_abonnement'),
    path('supprimer/<int:abonnement_id>/', views.supprimer_abonnement, name='supprimer_abonnement'),
    path('success/', views.page_de_succes, name='page_de_succes'),
    path('cancel/', views.page_annulation, name='page_annulation'),
    path('modifier-prix/<int:id>/', modifier_prix_abonnement, name='modifier_prix_abonnement'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
]
