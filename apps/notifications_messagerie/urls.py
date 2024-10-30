from django.urls import path
from .views import notifications_view, mark_as_read
from apps.notifications_messagerie.views import notifications_list
from . import views
app_name = 'notifications_messagerie'

urlpatterns = [
    path('notifications/', notifications_view, name='notifications'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('list/', views.notifications_list, name='notifications_list'), 
]
