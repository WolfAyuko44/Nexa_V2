from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Achat
from .forms import ArticleForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponse

def boutique(request):
    categorie_selectionnee = request.GET.get('categorie', '')
    articles = Article.objects.filter(categorie=categorie_selectionnee) if categorie_selectionnee else Article.objects.all()
    categories = [choice[0] for choice in Article.CATEGORIES]
    
    return render(request, 'monétisation/boutique.html', {
        'articles': articles,
        'categories': categories,
        'categorie_selectionnee': categorie_selectionnee,
    })

def article_detail(request, article_id):
    # Récupérer l'article demandé
    article = get_object_or_404(Article, id=article_id)
    
    # Préparer le contexte pour le template
    context = {
        'article': article,
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY  # Passer la clé publique Stripe au template
    }
    
    # Rendre le template avec le contexte
    return render(request, 'monétisation/article_detail.html', context)

@require_POST
def acheter_article(request):
    article_id = request.POST.get('article_id')
    stripe_token = request.POST.get('stripeToken')
    
    article = get_object_or_404(Article, id=article_id)

    if not stripe_token:
        return HttpResponse("Erreur : Token Stripe non fourni.", status=400)

    try:
        # Créez un paiement avec Stripe
        charge = stripe.Charge.create(
            amount=int(article.prix * 100),  # Montant en centimes
            currency='eur',
            description=f'Achat de {article.nom}',
            source=stripe_token,
        )

        # Enregistrez l'achat dans la base de données
        achat = Achat(
            utilisateur=request.user,
            article=article,
            quantite=1
        )
        achat.save()

        return redirect('monétisation:achats')

    except stripe.error.CardError as e:
        # Gérer les erreurs de carte
        return render(request, 'monétisation/erreur.html', {'message': str(e)})

    except stripe.error.StripeError as e:
        # Gérer les autres erreurs Stripe
        return render(request, 'monétisation/erreur.html', {'message': 'Une erreur est survenue lors du paiement.'})

@login_required
def achats(request):
    achats = Achat.objects.filter(utilisateur=request.user).select_related('article').order_by('-date_achat')
    return render(request, 'monétisation/achats.html', {'achats': achats})

@login_required
def ajouter_article(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('monétisation:boutique')
    else:
        form = ArticleForm()
    
    return render(request, 'monétisation/ajouter_article.html', {'form': form})

def create_checkout_session(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    try:
        # Créez une session de paiement Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': article.nom,
                        },
                        'unit_amount': int(article.prix * 100),  # Convertir le prix en centimes
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Ici, vous pouvez créer un achat ou effectuer toute autre action nécessaire

    return JsonResponse({'status': 'success'}, status=200)

@receiver(post_save, sender=Article)
def update_stripe_product(sender, instance, created, **kwargs):
    instance.save()  # Cela appellera la méthode save() avec la logique Stripe

@receiver(post_delete, sender=Article)
def delete_stripe_product(sender, instance, **kwargs):
    instance.delete()  # Cela appellera la méthode delete() avec la logique Stripe

