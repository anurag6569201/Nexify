# Generated by Django 5.1.2 on 2024-11-07 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_form_image_question_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
