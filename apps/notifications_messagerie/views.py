from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import Http404
from django.contrib import messages

@login_required
def notifications_view(request):
    """Vue pour afficher les notifications de l'utilisateur."""
    notifications = request.user.notifications.all()
    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """Marquer une notification comme lue."""
    try:
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        messages.success(request, "Notification marquée comme lue.")
    except Notification.DoesNotExist:
        messages.error(request, "Notification introuvable.")
    return redirect('notifications_messagerie:notifications')

@login_required
def notifications_list(request):
    """Vue pour afficher la liste des notifications."""
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, 'notifications_messagerie/notifications_list.html', {'notifications': notifications})
