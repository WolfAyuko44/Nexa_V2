from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, URLValidator, MaxLengthValidator

class Utilisateur(AbstractUser):
    # Avatar et biographie
    avatar = models.ImageField(
        upload_to='utilisateurs/avatars/', 
        blank=True, 
        null=True, 
        verbose_name=_("Avatar")
    )
    bio = models.TextField(
        blank=True, 
        null=True, 
        validators=[MaxLengthValidator(500)], 
        verbose_name=_("Biographie")
    )
    site_web = models.URLField(
        blank=True, 
        null=True, 
        validators=[URLValidator()], 
        verbose_name=_("Site Web")
    )
    localisation = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_("Localisation")
    )

    # Informations personnelles
    dob = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_("Date de Naissance")
    )
    gender = models.CharField(
        max_length=10, 
        choices=[
            ('male', _('Homme')), 
            ('female', _('Femme')), 
            ('other', _('Autre'))
        ], 
        blank=True, 
        null=True, 
        verbose_name=_("Genre")
    )
    nationality = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_("Nationalité")
    )

    # Informations de contact
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        null=True, 
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],  # Format international
        verbose_name=_("Numéro de téléphone")
    )

    # Relations (amis, abonnements)
    amis = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='amitiés', 
        blank=True, 
        verbose_name=_("Amis")
    )
    abonnements_relation = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='abonnés', 
        blank=True, 
        verbose_name=_("Abonnements")
    )

    # Notifications et paramètres de confidentialité
    notifications_non_lues = models.PositiveIntegerField(
        default=0, 
        verbose_name=_("Notifications Non Lues")
    )
    profil_public = models.BooleanField(
        default=True, 
        verbose_name=_("Profil Public")
    )
    affichage_statistiques = models.BooleanField(
        default=True, 
        verbose_name=_("Afficher Statistiques")
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

    def get_full_name(self):
        """Retourne le nom complet ou le nom d'utilisateur."""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_avatar_url(self):
        """Retourne l'URL de l'avatar ou un avatar par défaut."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/img/default-avatar.png'

    def save(self, *args, **kwargs):
        """Override save method for additional actions if necessary."""
        super().save(*args, **kwargs)

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator

class Post(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    description = models.TextField(
        max_length=500, 
        blank=True, 
        validators=[MaxLengthValidator(500)], 
        verbose_name=_("Description")
    )
    image = models.ImageField(
        upload_to='posts/images/', 
        blank=True, 
        null=True, 
        verbose_name=_("Image")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name=_("Date de Création")
    )

    # Champ pour les likes
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='liked_posts', 
        blank=True, 
        verbose_name=_("Likes")
    )

    def __str__(self):
        return f"Post by {self.utilisateur.username} - {self.description[:20]}"

    # Méthodes pour gérer les likes
    def total_likes(self):
        return self.likes.count()

    def liked_by_user(self, user):
        return self.likes.filter(id=user.id).exists()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-created_at']  # Les posts les plus récents d'abord

    def save(self, *args, **kwargs):
        """Override save method for additional actions if necessary."""
        super().save(*args, **kwargs)

