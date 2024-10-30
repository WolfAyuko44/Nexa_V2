# apps/messagerie/urls.py

from django.urls import path
from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation_list'),
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('compose/', views.compose_message, name='compose_message'),
]
