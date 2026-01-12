from django.db import models
from django.contrib.auth.models import User
from exchanges.models import ExchangeRequest
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    exchange_request = models.ForeignKey(ExchangeRequest, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['reviewer', 'exchange_request']
    
    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewed_user.username} - {self.rating} stars"
