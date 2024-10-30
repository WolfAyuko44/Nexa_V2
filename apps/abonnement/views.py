from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Abonnement, TypeAbonnement
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import Http404
import stripe

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request):
    # Créez une session de paiement Stripe
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Abonnement Premium',
                    },
                    'unit_amount': 1499,  # 14,99 € en centimes
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://127.0.0.1:8000/success/',
        cancel_url='http://127.0.0.1:8000/cancel/',
    )
    return redirect(session.url, code=303)

def souscrire_abonnement(request):
    if request.method == 'POST':
        # Traitement du paiement
        token = request.POST.get('stripeToken')  # Obtenu via le formulaire Stripe

        try:
            charge = stripe.Charge.create(
                amount=2999,  # 29.99 € en centimes
                currency='eur',
                description='Abonnement Premium',
                source=token,
            )
            # Logique après le paiement (comme l'enregistrement de l'abonnement)
            messages.success(request, "Vous avez souscrit avec succès à l'abonnement Premium !")
            return redirect('some_view_name')  # Redirigez vers une vue appropriée
        except stripe.error.StripeError:
            messages.error(request, "Une erreur s'est produite lors du traitement du paiement.")
            return redirect('souscrire_abonnement')

    return render(request, 'abonnement/souscrire_abonnement.html')

@login_required
def abonnement_detail(request):
    """
    Vue pour afficher les détails de l'abonnement actuel de l'utilisateur.
    """
    try:
        abonnement = get_object_or_404(Abonnement, utilisateur=request.user)
        return render(request, 'abonnement/abonnement_detail.html', {'abonnement': abonnement})
    except Http404:
        messages.error(request, "Vous n'avez pas d'abonnement actif. Veuillez souscrire à un abonnement.")
        return redirect('abonnement:souscrire_abonnement')  # Redirige vers la page de souscription


@login_required
def modifier_abonnement(request, abonnement_id):
    """
    Vue pour permettre à un utilisateur de modifier son abonnement.
    """
    abonnement = get_object_or_404(Abonnement, id=abonnement_id)
    types_abonnement = TypeAbonnement.objects.all()

    if request.method == "POST":
        type_abonnement_id = request.POST.get('type_abonnement')
        
        if not type_abonnement_id:
            messages.error(request, "Veuillez sélectionner un type d'abonnement.")
            return redirect('abonnement:modifier_abonnement', abonnement_id=abonnement_id)
        
        type_abonnement = get_object_or_404(TypeAbonnement, id=type_abonnement_id)
        
        # Mettre à jour les informations de l'abonnement
        abonnement.type_abonnement = type_abonnement
        abonnement.date_fin = timezone.now() + timezone.timedelta(days=type_abonnement.duree_jours)
        abonnement.save()
        
        messages.success(request, 'Votre abonnement a été modifié avec succès !')
        return redirect('abonnement:abonnement_detail')

    return render(request, 'abonnement/modifier_abonnement.html', {
        'abonnement': abonnement,
        'types_abonnement': types_abonnement
    })

@login_required
def supprimer_abonnement(request, abonnement_id):
    """
    Vue pour permettre à un utilisateur de supprimer son abonnement.
    """
    abonnement = get_object_or_404(Abonnement, id=abonnement_id)

    # Supprimer l'abonnement
    abonnement.delete()
    messages.success(request, 'Votre abonnement a été supprimé avec succès !')
    return redirect('abonnement:page_de_succes')

@login_required
def page_de_succes(request):
    """
    Vue pour afficher une page de succès après une action réussie.
    """
    return render(request, 'abonnement/page_de_succes.html')

@login_required
def page_annulation(request):
    """
    Vue pour afficher la page d'annulation d'abonnement.
    """
    if request.method == 'POST':
        motif = request.POST.get('motif')
        utilisateur = request.user
        abonnement = Abonnement.objects.filter(utilisateur=utilisateur).first()
        
        if abonnement:
            abonnement.delete()  # Supprime l'abonnement
            messages.success(request, 'Votre abonnement a été annulé avec succès !')
        else:
            messages.error(request, "Aucun abonnement trouvé à annuler.")
        
        return redirect('abonnement:page_de_succes')  # Redirection après l'annulation
    
    return render(request, 'abonnement/page_annulation.html')

def modifier_prix_abonnement(request, id):
    abonnement = get_object_or_404(Abonnement, id=id)  # Récupérez l'abonnement par son ID

    if request.method == 'POST':
        # Récupérez le nouveau prix depuis le formulaire
        nouveau_prix = request.POST.get('prix')

        # Mettez à jour le prix de l'abonnement
        abonnement.prix = nouveau_prix
        abonnement.save()  # Enregistrez les modifications

        return redirect('abonnement:abonnement_detail')  # Redirigez vers la page de détail de l'abonnement

    return render(request, 'modifier_prix.html', {'abonnement': abonnement})  # Renvoyez le modèle