from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message
from exchanges.models import ExchangeRequest
from .forms import MessageForm

@login_required
def conversation_list(request):
    # Get all exchanges where user is involved and status is accepted or completed
    exchanges = ExchangeRequest.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).filter(
        Q(status='accepted') | Q(status='completed')
    ).select_related('sender', 'receiver', 'skill_offered', 'skill_requested')
    
    # Get unread message count for each exchange
    conversations = []
    for exchange in exchanges:
        unread_count = Message.objects.filter(
            exchange_request=exchange,
            receiver=request.user,
            is_read=False
        ).count()
        
        # Get last message
        last_message = Message.objects.filter(exchange_request=exchange).order_by('-created_at').first()
        
        conversations.append({
            'exchange': exchange,
            'unread_count': unread_count,
            'last_message': last_message,
        })
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'messaging/conversation_list.html', context)

@login_required
def conversation_detail(request, exchange_id):
    exchange = get_object_or_404(ExchangeRequest, pk=exchange_id)
    
    # Check if user is part of this exchange
    if exchange.sender != request.user and exchange.receiver != request.user:
        messages.error(request, "You don't have permission to view this conversation.")
        return redirect('messaging:conversation_list')
    
    # Check if exchange is accepted or completed
    if exchange.status not in ['accepted', 'completed']:
        messages.warning(request, "You can only message when an exchange is accepted.")
        return redirect('exchanges:request_detail', pk=exchange_id)
    
    # Mark all messages in this conversation as read
    Message.objects.filter(
        exchange_request=exchange,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    # Get all messages for this exchange
    conversation_messages = Message.objects.filter(
        exchange_request=exchange
    ).select_related('sender', 'receiver').order_by('created_at')
    
    # Handle message sending
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = exchange.sender if exchange.receiver == request.user else exchange.receiver
            message.exchange_request = exchange
            message.save()
            messages.success(request, 'Message sent!')
            return redirect('messaging:conversation_detail', exchange_id=exchange_id)
    else:
        form = MessageForm()
    
    context = {
        'exchange': exchange,
        'messages': conversation_messages,
        'form': form,
        'other_user': exchange.sender if exchange.receiver == request.user else exchange.receiver,
    }
    return render(request, 'messaging/conversation_detail.html', context)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, sender=request.user)
    exchange_id = message.exchange_request.id
    message.delete()
    messages.success(request, 'Message deleted.')
    return redirect('messaging:conversation_detail', exchange_id=exchange_id)
