# Generated by Django 5.1.2 on 2024-11-08 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tender_name', models.CharField(max_length=255, verbose_name='Tender Name')),
                ('tender_id', models.CharField(max_length=100, unique=True, verbose_name='Tender ID')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('issued_by', models.CharField(max_length=255, verbose_name='Issued By')),
                ('version', models.PositiveIntegerField(default=1, verbose_name='Version')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('bid_submission_deadline', models.DateTimeField(blank=True, null=True, verbose_name='Last Date & Time of Submission of Bids')),
                ('technical_bid_opening', models.DateTimeField(blank=True, null=True, verbose_name='Date & Time of Opening of Technical Bids')),
                ('financial_bid_opening', models.DateTimeField(blank=True, null=True, verbose_name='Date & Time of Opening of Financial Bids')),
                ('publication_details', models.TextField(blank=True, null=True, verbose_name='Details of Publication in the Print Media')),
                ('website_publication_date', models.DateField(blank=True, null=True, verbose_name='Date of Publication on the Institute Website')),
                ('tender_document', models.FileField(blank=True, null=True, upload_to='tenders/', verbose_name='Tender Document')),
                ('document_link', models.URLField(blank=True, max_length=500, null=True, verbose_name='Link to Download Tender Documents')),
                ('is_extended', models.BooleanField(default=False, verbose_name='Is Deadline Extended?')),
                ('extended_bid_submission_deadline', models.DateTimeField(blank=True, null=True, verbose_name='Extended Last Date & Time of Submission of Bids')),
                ('reminder_enabled', models.BooleanField(default=False, verbose_name='Enable Reminder?')),
                ('reminder_period', models.DurationField(blank=True, null=True, verbose_name='Reminder Period (e.g., 3 days before)')),
                ('reminder_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email for Reminder')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
        ),
        migrations.CreateModel(
            name='TenderField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=255, verbose_name='Field Name')),
                ('field_value', models.TextField(verbose_name='Field Value')),
                ('tender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extendable_fields', to='tenders.tender')),
            ],
            options={
                'verbose_name': 'Tender Field',
                'verbose_name_plural': 'Tender Fields',
            },
        ),
    ]
