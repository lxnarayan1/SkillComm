from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from exchanges.models import ExchangeRequest
from .forms import ReviewForm

@login_required
def create_review(request, exchange_id):
    exchange = get_object_or_404(ExchangeRequest, pk=exchange_id)
    
    # Check if user is part of this exchange
    if exchange.sender != request.user and exchange.receiver != request.user:
        messages.error(request, "You don't have permission to review this exchange.")
        return redirect('accounts:dashboard')
    
    # Check if exchange is completed
    if exchange.status != 'completed':
        messages.warning(request, "You can only review completed exchanges.")
        return redirect('exchanges:request_detail', pk=exchange_id)
    
    # Determine who to review
    reviewed_user = exchange.sender if exchange.receiver == request.user else exchange.receiver
    
    # Check if user already reviewed this exchange
    existing_review = Review.objects.filter(
        reviewer=request.user,
        exchange_request=exchange
    ).first()
    
    if existing_review:
        messages.info(request, "You have already reviewed this exchange.")
        return redirect('exchanges:request_detail', pk=exchange_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.exchange_request = exchange
            review.save()
            messages.success(request, f'Review submitted for {reviewed_user.username}!')
            return redirect('accounts:profile', username=reviewed_user.username)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'exchange': exchange,
        'reviewed_user': reviewed_user,
    }
    return render(request, 'reviews/create_review.html', context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, reviewer=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated!')
            return redirect('accounts:profile', username=review.reviewed_user.username)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
        'is_edit': True,
    }
    return render(request, 'reviews/create_review.html', context)

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, reviewer=request.user)
    reviewed_user_username = review.reviewed_user.username
    review.delete()
    messages.success(request, 'Review deleted.')
    return redirect('accounts:profile', username=reviewed_user_username)

@login_required
def my_reviews(request):
    given_reviews = Review.objects.filter(reviewer=request.user).select_related('reviewed_user', 'exchange_request')
    received_reviews = Review.objects.filter(reviewed_user=request.user).select_related('reviewer', 'exchange_request')
    
    context = {
        'given_reviews': given_reviews,
        'received_reviews': received_reviews,
    }
    return render(request, 'reviews/my_reviews.html', context)
