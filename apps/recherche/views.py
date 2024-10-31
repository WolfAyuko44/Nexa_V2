# apps/recherche/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def recherche_utilisateur(request):
    query = request.GET.get('q', '')  # Récupère la valeur de la requête 'q'
    utilisateurs = User.objects.all()  # Récupère tous les utilisateurs par défaut

    if query:
        # Filtre les utilisateurs en fonction de la requête
        utilisateurs = utilisateurs.filter(username__icontains=query)

    return render(request, 'recherche/recherche_utilisateur.html', {'utilisateurs': utilisateurs, 'query': query})
