from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.utilisateurs.models import Post

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',  # Relation pour accéder aux commentaires depuis un post
        on_delete=models.CASCADE
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments_partage_contenu',  # Relation inverse pour accéder aux commentaires d'un utilisateur
        null=True  # Permettre des valeurs nulles
    )
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    modifié = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.utilisateur.username} - {self.texte[:20]}"

    def edit_comment(self, new_text):
        """Permet de modifier le texte du commentaire."""
        self.texte = new_text
        self.modifié = True
        self.save()

class Like(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='likes_in_partage_contenu',  # Changer le related_name pour éviter les conflits
        on_delete=models.CASCADE
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes_partage_contenu',  # Relation inverse pour accéder aux likes d'un utilisateur
        null=True  # Permettre des valeurs nulles
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'utilisateur')  # Empêcher qu'un utilisateur aime plusieurs fois le même post

    def __str__(self):
        return f"{self.utilisateur.username} aime {self.post.titre}"
