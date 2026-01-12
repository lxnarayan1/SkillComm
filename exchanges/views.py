from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ExchangeRequest
from .forms import ExchangeRequestForm

@login_required
def send_request(request, username):
    receiver = get_object_or_404(User, username=username)
    
    if receiver == request.user:
        messages.error(request, "You cannot send a request to yourself!")
        return redirect('skills:browse_users')
    
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST, sender=request.user, receiver=receiver)
        if form.is_valid():
            exchange = form.save(commit=False)
            exchange.sender = request.user
            exchange.receiver = receiver
            exchange.save()
            messages.success(request, f'Exchange request sent to {receiver.username}!')
            return redirect('accounts:dashboard')
    else:
        form = ExchangeRequestForm(sender=request.user, receiver=receiver)
    
    context = {
        'form': form,
        'receiver': receiver,
    }
    return render(request, 'exchanges/send_request.html', context)

@login_required
def request_detail(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk)
    
    # Check if user is part of this exchange
    if exchange.sender != request.user and exchange.receiver != request.user:
        messages.error(request, "You don't have permission to view this request.")
        return redirect('accounts:dashboard')
    
    context = {
        'exchange': exchange,
    }
    return render(request, 'exchanges/request_detail.html', context)

@login_required
def accept_request(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk, receiver=request.user)
    
    if exchange.status == 'pending':
        exchange.status = 'accepted'
        exchange.save()
        messages.success(request, 'Exchange request accepted!')
    else:
        messages.warning(request, 'This request is no longer pending.')
    
    return redirect('exchanges:request_detail', pk=pk)

@login_required
def decline_request(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk, receiver=request.user)
    
    if exchange.status == 'pending':
        exchange.status = 'declined'
        exchange.save()
        messages.info(request, 'Exchange request declined.')
    else:
        messages.warning(request, 'This request is no longer pending.')
    
    return redirect('accounts:dashboard')

@login_required
def complete_request(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk)
    
    # Both sender and receiver can mark as complete
    if exchange.sender != request.user and exchange.receiver != request.user:
        messages.error(request, "You don't have permission to modify this request.")
        return redirect('accounts:dashboard')
    
    if exchange.status == 'accepted':
        exchange.status = 'completed'
        exchange.save()
        messages.success(request, 'Exchange marked as completed! You can now leave a review.')
    else:
        messages.warning(request, 'This request cannot be marked as completed.')
    
    return redirect('exchanges:request_detail', pk=pk)

@login_required
def cancel_request(request, pk):
    exchange = get_object_or_404(ExchangeRequest, pk=pk, sender=request.user)
    
    if exchange.status == 'pending':
        exchange.status = 'cancelled'
        exchange.save()
        messages.info(request, 'Exchange request cancelled.')
    else:
        messages.warning(request, 'This request cannot be cancelled.')
    
    return redirect('accounts:dashboard')

@login_required
def my_exchanges(request):
    sent = request.user.sent_requests.all()
    received = request.user.received_requests.all()
    
    context = {
        'sent_requests': sent,
        'received_requests': received,
    }
    return render(request, 'exchanges/my_exchanges.html', context)