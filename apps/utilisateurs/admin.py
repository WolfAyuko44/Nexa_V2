from django.contrib import admin
from django.utils.html import format_html
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'get_full_name', 'email', 'profil_public', 'get_avatar', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('profil_public', 'abonnements_relation', 'amis', 'gender', 'nationality')
    ordering = ('date_joined',)
    readonly_fields = ('get_avatar',)

    def get_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "Pas d'avatar"

    get_avatar.short_description = 'Avatar'

    def get_queryset(self, request):
        """Pour afficher les utilisateurs avec la date d'inscription."""
        qs = super().get_queryset(request)
        return qs.annotate(date_joined=F('date_joined'))

    def date_joined(self, obj):
        """Affiche la date à laquelle l'utilisateur a rejoint."""
        return obj.date_joined.strftime('%Y-%m-%d') if obj.date_joined else "N/A"

    date_joined.admin_order_field = 'date_joined'  # Permet de trier par cette colonne
    date_joined.short_description = 'Date d\'inscription'
