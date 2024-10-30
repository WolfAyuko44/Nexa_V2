from django.contrib import admin
from .models import Article, Achat

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'prix')
    search_fields = ('nom', 'description')
    list_filter = ('categorie',)

@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'article', 'quantite', 'date_achat')
    search_fields = ('utilisateur__username', 'article__nom')
    list_filter = ('date_achat',)
