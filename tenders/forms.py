from django import forms
from django.forms import modelformset_factory
from .models import Tender, TenderField

class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = [
            'tender_name', 'tender_id', 'start_date', 'issued_by',
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
