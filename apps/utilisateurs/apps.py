from django.apps import AppConfig

class UtilisateursConfig(AppConfig):
    name = 'apps.utilisateurs'

    def ready(self):
        # Importer les signaux
        import apps.utilisateurs.signals
