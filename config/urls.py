from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.utilisateurs.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('utilisateurs/', include('apps.utilisateurs.urls')),
    path('matchmaking/', include('apps.matchmaking.urls')),
    path('partage_contenu/', include('apps.partage_contenu.urls')),
    path('notifications_messagerie/', include('apps.notifications_messagerie.urls')),
    path('abonnement/', include('apps.abonnement.urls')),
    path('monetisation/', include('apps.monétisation.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('messagerie/', include('apps.messagerie.urls')),
    path('user_settings/', include('apps.user_settings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
