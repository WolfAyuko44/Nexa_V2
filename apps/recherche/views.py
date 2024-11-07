# apps/recherche/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def recherche_utilisateur(request):
    query = request.GET.get('q', '').strip()  # Récupère la valeur de la requête 'q' et enlève les espaces
    utilisateurs = User.objects.all()  # Récupère tous les utilisateurs par défaut

    if query:
        # Filtre les utilisateurs en fonction de la requête
        utilisateurs = utilisateurs.filter(username__icontains=query)

    # Pour déboguer : afficher le nombre d'utilisateurs trouvés
    print(f"Nombre d'utilisateurs trouvés : {utilisateurs.count()}")  # Debug

    return render(request, 'recherche/recherche_utilisateur.html', {'utilisateurs': utilisateurs, 'query': query})
