from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from .forms import (
    BaseInfoForm,
    PersonalInfoForm,
    ContactInfoForm,
    PrivacySettingsForm,
    SecurityForm,
    ProfilePictureForm,
)
from apps.utilisateurs.models import Utilisateur

@login_required
def base_info_settings(request):
    if request.method == 'POST':
        form = BaseInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Informations mises à jour avec succès.')
            return redirect(reverse('user_settings:settings'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(form.errors, status=400)
            messages.error(request, 'Erreur lors de la mise à jour des informations.')
    else:
        form = BaseInfoForm(instance=request.user)
    
    return render(request, 'settings/base_info.html', {'base_info_form': form})


@login_required
def personal_info_settings(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations personnelles mises à jour.')
            return redirect(reverse('user_settings:settings'))
    else:
        form = PersonalInfoForm(instance=request.user)
    
    return render(request, 'settings/personal_info.html', {'form': form})

@login_required
def contact_info_settings(request):
    if request.method == 'POST':
        form = ContactInfoForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informations de contact mises à jour.')
            return redirect(reverse('user_settings:settings'))
    else:
        form = ContactInfoForm(instance=request.user)
    
    return render(request, 'settings/settings_contact_info.html', {'form': form})

@login_required
def privacy_settings(request):
    user = get_object_or_404(Utilisateur, id=request.user.id)
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Préférences de confidentialité mises à jour.')
            return redirect(reverse('user_settings:settings'))
    else:
        form = PrivacySettingsForm(instance=user)
    
    return render(request, 'settings/settings_privacy_settings.html', {'form': form})

@login_required
def security_settings(request):
    if request.method == 'POST':
        form = SecurityForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            
            user = request.user
            if not user.check_password(old_password):
                form.add_error('old_password', 'Ancien mot de passe incorrect.')
            elif new_password != confirm_password:
                form.add_error('confirm_password', 'Les mots de passe ne correspondent pas.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Mot de passe mis à jour.')
                return redirect(reverse('user_settings:settings'))
    else:
        form = SecurityForm()
    
    return render(request, 'settings/settings_security_authentication.html', {'form': form})

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Photo de profil mise à jour.')
            return redirect(reverse('user_settings:settings'))
    else:
        form = ProfilePictureForm(instance=request.user)
    
    return render(request, 'upload.html', {'form': form})

@login_required
def settings_view(request):
    user = request.user

    forms = {
        'base_info': BaseInfoForm(instance=user),
        'personal_info': PersonalInfoForm(instance=user),
        'contact_info': ContactInfoForm(instance=user),
        'privacy_settings': PrivacySettingsForm(instance=user),
        'security_settings': SecurityForm()
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type in forms:
            form = forms[form_type]
            if form.is_valid():
                form.save()
                messages.success(request, 'Paramètres mis à jour avec succès.')
                return redirect(reverse('user_settings:settings'))

    return render(request, 'settings/settings.html', {
        'forms': forms,
        'username': user.username,
    })
