from django.db import models
from django.contrib.auth.models import User
from skills.models import Skill

class ExchangeRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    skill_offered = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='offered_in_exchanges')
    skill_requested = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='requested_in_exchanges')
    message = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.skill_offered.name} for {self.skill_requested.name}"
    
    def can_review(self, user):
        """Check if user can review this exchange"""
        return self.status == 'completed' and (user == self.sender or user == self.receiver)
