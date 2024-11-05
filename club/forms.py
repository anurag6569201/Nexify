from club import models
from django import forms

class ClubDataForm(forms.ModelForm):
    class Meta:
        model = models.ClubData
        fields = ['json_data']  
        widgets = {
            'json_data': forms.Textarea(attrs={'rows': 10, 'cols': 80}), 
        }