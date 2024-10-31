from django.test import TestCase
from django.urls import reverse
from apps.utilisateurs.models import Utilisateur

class RechercheUtilisateurTest(TestCase):
    def setUp(self):
        self.utilisateur = Utilisateur.objects.create_user(username='testuser', password='testpassword')

    def test_recherche_utilisateur(self):
        response = self.client.get(reverse('recherche:recherche_utilisateur'), {'q': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
