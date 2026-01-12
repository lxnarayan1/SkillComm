from django import forms
from .models import ExchangeRequest

class ExchangeRequestForm(forms.ModelForm):
    class Meta:
        model = ExchangeRequest
        fields = ['skill_offered', 'skill_requested', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Introduce yourself and explain what you hope to learn...'}),
        }
    
    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        receiver = kwargs.pop('receiver', None)
        super().__init__(*args, **kwargs)
        
        # Limit skill_offered to sender's teaching skills
        if sender:
            self.fields['skill_offered'].queryset = sender.profile.skills_to_teach.all()
            self.fields['skill_offered'].label = "I will teach"
        
        # Limit skill_requested to receiver's teaching skills
        if receiver:
            self.fields['skill_requested'].queryset = receiver.profile.skills_to_teach.all()
            self.fields['skill_requested'].label = "I want to learn"
        
        # Make message optional
        self.fields['message'].required = False