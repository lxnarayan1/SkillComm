from django.db import models

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technology', 'Technology'),
        ('language', 'Language'),
        ('music', 'Music'),
        ('art', 'Art & Design'),
        ('fitness', 'Fitness & Sports'),
        ('cooking', 'Cooking & Culinary'),
        ('business', 'Business & Finance'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_teachers_count(self):
        return self.teachers.count()
    
    def get_learners_count(self):
        return self.learners.count()
