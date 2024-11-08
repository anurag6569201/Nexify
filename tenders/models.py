from django.db import models

class Tender(models.Model):
    # Essential Fields (Cannot be null)
    tender_name = models.CharField(max_length=255, verbose_name="Tender Name")
    tender_id = models.CharField(max_length=100, unique=True, verbose_name="Tender ID")
    start_date = models.DateField(verbose_name="Start Date")
    issued_by = models.CharField(max_length=255, verbose_name="Issued By")

    # Versioning and Active Status
    version = models.PositiveIntegerField(default=1, verbose_name="Version")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    # Optional Fields (Can be null)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    end_date = models.DateField(blank=True, null=True, verbose_name="End Date")
    bid_submission_deadline = models.DateTimeField(blank=True, null=True, verbose_name="Last Date & Time of Submission of Bids")
    technical_bid_opening = models.DateTimeField(blank=True, null=True, verbose_name="Date & Time of Opening of Technical Bids")
    financial_bid_opening = models.DateTimeField(blank=True, null=True, verbose_name="Date & Time of Opening of Financial Bids")
    publication_details = models.TextField(blank=True, null=True, verbose_name="Details of Publication in the Print Media")
    website_publication_date = models.DateField(blank=True, null=True, verbose_name="Date of Publication on the Institute Website")
    tender_document = models.FileField(upload_to='tenders/', blank=True, null=True, verbose_name="Tender Document")
    document_link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Link to Download Tender Documents")
    is_extended = models.BooleanField(default=False, verbose_name="Is Deadline Extended?")
    extended_bid_submission_deadline = models.DateTimeField(blank=True, null=True, verbose_name="Extended Last Date & Time of Submission of Bids")

    # Reminder Fields
    reminder_enabled = models.BooleanField(default=False, verbose_name="Enable Reminder?")
    reminder_period = models.DurationField(blank=True, null=True, verbose_name="Reminder Period (e.g., 3 days before)")
    reminder_email = models.EmailField(blank=True, null=True, verbose_name="Email for Reminder")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.tender_name

class TenderField(models.Model):
    tender = models.ForeignKey(Tender, related_name='extendable_fields', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255, verbose_name="Field Name")
    field_value = models.TextField(verbose_name="Field Value")

    class Meta:
        verbose_name = "Tender Field"
        verbose_name_plural = "Tender Fields"

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"
