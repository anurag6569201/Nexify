from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import timedelta
from .models import Tender, TenderField
from .forms import TenderForm, TenderFieldForm, TenderFieldFormSet

# View all tenders
def tender_list(request):
    tenders = Tender.objects.all()
    return render(request, 'tenders/tender_list.html', {'tenders': tenders})

# View tender details (including previous versions)
def tender_detail(request, tender_id):
    tender = get_object_or_404(Tender, id=tender_id)
    previous_tenders = Tender.objects.filter(tender_name=tender.tender_name).exclude(id=tender_id)
    return render(request, 'tenders/tender_detail.html', {'tender': tender, 'previous_tenders': previous_tenders})

# Add or update a tender along with extendable fields
def add_tender(request):
    if request.method == 'POST':
        # Handling the tender form and field formset simultaneously
        form = TenderForm(request.POST, request.FILES)
        tender_field_formset = TenderFieldFormSet(request.POST)

        if form.is_valid() and tender_field_formset.is_valid():
            # Save the Tender
            tender = form.save()

            # Save the extendable fields
            for tender_field_form in tender_field_formset:
                field_name = tender_field_form.cleaned_data.get('field_name')
                field_value = tender_field_form.cleaned_data.get('field_value')

                if field_name and field_value:
                    TenderField.objects.create(tender=tender, field_name=field_name, field_value=field_value)

            # Check if reminder is enabled and if reminder date has arrived
            if tender.reminder_enabled:
                reminder_date = tender.end_date - timedelta(days=tender.reminder_period.days)
                if timezone.now().date() >= reminder_date:
                    send_reminder_email(tender)

            messages.success(request, "Tender and extendable fields successfully created!")
            return redirect('tender_list')
        else:
            print("Form is not valid!")
            # Print all errors for debugging
            print(form.errors)
            print(tender_field_formset.errors)
    else:
        form = TenderForm()
        tender_field_formset = TenderFieldFormSet(queryset=TenderField.objects.none())

    return render(request, 'tenders/add_tender_and_field.html', {
        'form': form, 'tender_field_formset': tender_field_formset
    })


# Send reminder email
def send_reminder_email(tender):
    subject = f"Reminder: Tender '{tender.tender_name}' is about to end"
    message = f"Dear User,\n\nThis is a reminder that the tender '{tender.tender_name}' is scheduled to end on {tender.end_date}. Please make sure to complete any required actions before the deadline.\n\nBest regards,\nTender Management Team"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [tender.reminder_email]

    send_mail(subject, message, from_email, recipient_list)
