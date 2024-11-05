from django import forms
from .models import Form, Question, Option

class FormForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']  # Removed 'form' since it's set in the view

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']  # Removed 'question' since it's set in the view
