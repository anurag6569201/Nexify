from django import forms
from .models import Form, Question

class FormCreateForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['form', 'text', 'question_type', 'choices']
        widgets = {
            'choices': forms.Textarea(attrs={'placeholder': 'Enter comma-separated choices for multiple-choice questions'}),
        }
