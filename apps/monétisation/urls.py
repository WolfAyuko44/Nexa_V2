# urls.py
from django.urls import path
from . import views

app_name = 'monétisation'

urlpatterns = [
    path('', views.boutique, name='boutique'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('acheter/<int:article_id>/', views.acheter_article, name='acheter_article'),
    path('achats/', views.achats, name='achats'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('create-checkout-session/<int:article_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
]
