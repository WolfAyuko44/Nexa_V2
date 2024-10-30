from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        """Initialisation des données pour les tests."""
        self.username = 'testuser'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_signup(self):
        """Test de l'inscription d'un nouvel utilisateur."""
        response = self.client.post(reverse('utilisateurs:signup'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        })
        print(response.content)  # Affiche le contenu de la réponse pour le débogage
        self.assertEqual(response.status_code, 302)  # Vérifiez la redirection
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Vérifiez que l'utilisateur a été créé


    def test_login(self):
        """Test de la connexion d'un utilisateur existant."""
        response = self.client.post(reverse('utilisateurs:connexion'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)  # Vérifiez la redirection
        self.assertEqual(str(response.wsgi_request.user), self.username)  # Vérifiez que l'utilisateur est connecté

    def test_logout(self):
        """Test de la déconnexion d'un utilisateur."""
        self.client.login(username=self.username, password=self.password)  # Connectez-vous d'abord
        response = self.client.get(reverse('utilisateurs:logout'))
        self.assertEqual(response.status_code, 302)  # Vérifiez la redirection
        self.assertEqual(str(response.wsgi_request.user), 'AnonymousUser')  # Vérifiez que l'utilisateur est déconnecté

    def test_access_protected_page(self):
        """Test d'accès à une page protégée après connexion."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('utilisateurs:profil_detail', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 200)  # Vérifiez que la page est accessible

    def test_access_protected_page_without_login(self):
        """Test d'accès à une page protégée sans connexion."""
        response = self.client.get(reverse('utilisateurs:profil_detail', kwargs={'username': self.username}))
        self.assertEqual(response.status_code, 302)  # Vérifiez la redirection vers la page de connexion

# Pour exécuter ces tests, utilisez la commande suivante dans le terminal :
# python manage.py test utilisateurs
