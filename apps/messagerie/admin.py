# apps/messagerie/admin.py

from django.contrib import admin
from .models import Conversation, Message

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')  # Assurez-vous que 'created_at' existe dans votre modèle

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'conversation', 'created_at')  # Assurez-vous que 'created_at' existe dans votre modèle

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
