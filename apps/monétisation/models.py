from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import stripe

class Article(models.Model):
    CATEGORIES = [
        ('Aura', 'Aura'),
        ('Bannière', 'Bannière'),
        ('Badge', 'Badge'),
        ('Skin', 'Skin'),
        ('Loot Box', 'Loot Box'),
    ]
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=20, choices=CATEGORIES)
    image = models.ImageField(upload_to='monetisation/articles/', blank=True, null=True)
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        if not self.stripe_product_id:
            # Créer le produit sur Stripe
            product = stripe.Product.create(
                name=self.nom,
                description=self.description,
            )
            self.stripe_product_id = product.id

            # Créer le prix associé au produit sur Stripe
            stripe.Price.create(
                product=self.stripe_product_id,
                unit_amount=int(self.prix * 100),  # Le montant est en centimes
                currency="usd",  # Adapter selon votre devise
            )
        else:
            # Mettre à jour le produit sur Stripe
            stripe.Product.modify(
                self.stripe_product_id,
                name=self.nom,
                description=self.description,
            )

        super(Article, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Supprimer le produit de Stripe
        if self.stripe_product_id:
            stripe.Product.delete(self.stripe_product_id)
        super(Article, self).delete(*args, **kwargs)

class Achat(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='achats')
    date_achat = models.DateTimeField(auto_now_add=True)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Achat de {self.article.nom} par {self.utilisateur.username}"
