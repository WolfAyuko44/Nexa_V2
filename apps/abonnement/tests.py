from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.abonnement.models import Abonnement, TypeAbonnement
from django.contrib.auth import get_user_model

class TestAbonnement(TestCase):
    def setUp(self):
        # Création d'un utilisateur de test
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='password')

        # Création d'un type d'abonnement Premium
        self.type_abonnement = TypeAbonnement.objects.create(nom='Premium', prix=14.99, duree_jours=30)

        # Création d'un abonnement actif
        self.abonnement = Abonnement.objects.create(
            utilisateur=self.user,
            type_abonnement=self.type_abonnement,
            date_fin=timezone.now() + timedelta(days=30)  # Abonnement actif pour 30 jours
        )

    def test_abonnement_creation(self):
        """Test pour s'assurer que l'abonnement est créé avec les bons attributs."""
        self.assertEqual(self.abonnement.utilisateur, self.user)
        self.assertEqual(self.abonnement.type_abonnement, self.type_abonnement)
        self.assertTrue(self.abonnement.est_active())  # Vérifiez que l'abonnement est actif

    def test_fonctionnalites_premium(self):
        """Test pour vérifier que les fonctionnalités Premium sont accessibles."""
        self.assertTrue(self.abonnement.est_active())
        self.assertEqual(self.abonnement.type_abonnement.nom, 'Premium')
        
        # Vérification d'accès à des fonctionnalités spécifiques
        # Vous pouvez ajouter des méthodes dans votre modèle pour ces vérifications
        # Exemple: self.assertTrue(self.user.has_access_to_exclusive_content())
        
    def test_abonnement_inactif(self):
        """Test pour vérifier que l'abonnement devient inactif après la date de fin."""
        # Simulez le passage du temps en avançant la date
        self.abonnement.date_fin = timezone.now() - timedelta(days=1)  # Abonnement expiré
        self.abonnement.save()  # Sauvegarde des changements

        self.assertFalse(self.abonnement.est_active())  # L'abonnement ne devrait plus être actif

    def test_date_fin_format(self):
        """Test pour vérifier que la date de fin est un datetime valide."""
        self.assertIsInstance(self.abonnement.date_fin, timezone.datetime)

    def tearDown(self):
        """Nettoyage après les tests si nécessaire."""
        self.abonnement.delete()
        self.type_abonnement.delete()
        self.user.delete()

