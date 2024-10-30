from django.urls import path
from .views import (
    base_info_settings,
    personal_info_settings,
    contact_info_settings,
    privacy_settings,
    security_settings,
    upload_profile_picture,
    settings_view,
)

app_name = 'user_settings'

urlpatterns = [
    # Settings URLs
    path('settings/base-info/', base_info_settings, name='base_info'),
    path('settings/personal-info/', personal_info_settings, name='personal_info'),
    path('settings/privacy-settings/', privacy_settings, name='privacy_settings'),
    path('settings/security-settings/', security_settings, name='security_settings'),
    path('settings/upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path('settings', settings_view, name='settings'),  
]
