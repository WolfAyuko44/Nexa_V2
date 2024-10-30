from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .forms import MessageForm
from django.views.generic import ListView

User = get_user_model()

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messagerie/inbox.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            return redirect('messagerie:conversation_detail', conversation_id=conversation_id)
    else:
        form = MessageForm()
    messages = conversation.messages.all()
    return render(request, 'messagerie/message_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

@login_required
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            recipient_usernames = request.POST.getlist('recipients')
            recipients = User.objects.filter(username__in=recipient_usernames)
            if recipients.exists():
                # Get or create a conversation
                conversation, created = Conversation.objects.get_or_create(
                    participants__in=[request.user, *recipients]
                )
                message = form.save(commit=False)
                message.sender = request.user
                message.conversation = conversation
                message.save()
                return redirect('messagerie:inbox')
    else:
        form = MessageForm()
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    return render(request, 'messagerie/compose.html', {'form': form, 'users': users})

class ConversationListView(ListView):
    model = Conversation
    template_name = 'messagerie/conversation_list.html'
    context_object_name = 'conversations'
