from django import forms
from django.forms import modelformset_factory
from .models import Tender, TenderField

from django import forms
from .models import Tender, TenderField

class TenderForm(forms.ModelForm):
    # Using DateInput with type="date" to ensure the date picker is shown in browsers
    start_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],  # Specify acceptable input format
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )
    end_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    )
    # bid_submission_deadline = forms.DateField(
    #     required=False,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    # )
    # technical_bid_opening = forms.DateField(
    #     required=False,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    # )
    # financial_bid_opening = forms.DateField(
    #     required=False,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    # )
    # website_publication_date = forms.DateField(
    #     required=False,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    # )
    # extended_bid_submission_deadline = forms.DateField(
    #     required=False,
    #     input_formats=['%Y-%m-%d'],
    #     widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'type': 'date'})
    # )

    class Meta:
        model = Tender
        fields = [
            'tender_name', 'tender_id', 'issued_by', 'start_date',
            'description', 'end_date', 'bid_submission_deadline',
            'technical_bid_opening', 'financial_bid_opening',
            'publication_details', 'website_publication_date',
            'tender_document', 'document_link', 'is_extended',
            'extended_bid_submission_deadline', 'reminder_enabled',
            'reminder_period', 'reminder_email'
        ]
class TenderFieldForm(forms.ModelForm):
    class Meta:
        model = TenderField
        fields = ['field_name', 'field_value']

# Dynamically create a formset for TenderField
TenderFieldFormSet = modelformset_factory(TenderField, form=TenderFieldForm, extra=1)
