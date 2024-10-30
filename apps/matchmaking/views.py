from django.shortcuts import render, get_object_or_404, redirect
from .models import MatchmakingRequest, ProfilUtilisateur
from .forms import MatchmakingRequestForm

def recherche_match(request):
    if request.method == 'POST':
        form = MatchmakingRequestForm(request.POST)
        if form.is_valid():
            matchmaking_request = form.save(commit=False)
            matchmaking_request.utilisateur = request.user
            matchmaking_request.save()
            return redirect('resultats')
    else:
        form = MatchmakingRequestForm()
    return render(request, 'matchmaking/recherche_match.html', {'form': form})

def resultats(request):
    # Exemple de logique pour récupérer les utilisateurs qui correspondent à la demande
    user_profile = ProfilUtilisateur.objects.get(utilisateur=request.user)
    matching_requests = MatchmakingRequest.objects.filter(
        niveau_recherche=user_profile.niveau,
        style_jeu_recherche=user_profile.style_jeu,
        region_recherche=user_profile.region,
        langue_recherche=user_profile.langue
    ).exclude(utilisateur=request.user)
    
    return render(request, 'matchmaking/resultats.html', {'matching_requests': matching_requests})
