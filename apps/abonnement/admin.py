# admin.py
from django.contrib import admin
from .models import Abonnement

class AbonnementAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type_abonnement', 'date_debut', 'date_fin', 'est_active', 'badge_abonnement')
    list_filter = ('type_abonnement', 'date_debut', 'date_fin', 'badge_abonnement')
    search_fields = ('utilisateur__username',)  # Recherche par nom d'utilisateur
    ordering = ('-date_debut',)

    # Optionnel : ajouter une action personnalisée pour supprimer des abonnements
    actions = ['supprimer_abonnement']

    def supprimer_abonnement(self, request, queryset):
        """Action pour supprimer les abonnements sélectionnés."""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} abonnement(s) supprimé(s).")

    supprimer_abonnement.short_description = "Supprimer les abonnements sélectionnés"

# Enregistrement du modèle avec l'admin
admin.site.register(Abonnement, AbonnementAdmin)
