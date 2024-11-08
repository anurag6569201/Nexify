from django import forms
from .models import PollSet, PollOption
from django import forms
from django.utils import timezone
from datetime import timedelta


class PollCreationForm(forms.ModelForm):
    options = forms.CharField(widget=forms.Textarea, help_text="Enter each option on a new line")
    closed_at = forms.DateTimeField(required=False)  # DateTimeField will handle the combined datetime

    class Meta:
        model = PollSet
        fields = ['title', 'closed_at']  # 'closed_at' will be filled with combined date and time

    def save(self, commit=True):
        poll = super().save(commit=False)
        
        # If closed_at is provided by the form, use it. Otherwise, set a default closing time.
        if self.cleaned_data['closed_at']:
            poll.closed_at = self.cleaned_data['closed_at']
        else:
            poll.closed_at = timezone.now() + timedelta(minutes=30)  # Default to 30 minutes from now
        
        if commit:
            poll.save()
            
            # Handle the options input (one option per line)
            options = self.cleaned_data['options'].splitlines()
            for option_text in options:
                if option_text.strip():  # Ensure it's not an empty line
                    PollOption.objects.create(poll=poll, text=option_text.strip())
        return poll


class VoteForm(forms.Form):
    option = forms.ModelChoiceField(queryset=PollOption.objects.none(), widget=forms.RadioSelect)
    
    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = poll.options.all()
