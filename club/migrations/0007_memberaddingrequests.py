# Generated by Django 5.1.2 on 2024-11-26 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("club", "0006_alter_clubdata_user"),
    ]

    operations = [
        migrations.CreateModel(
            name="MemberAddingRequests",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=100)),
                ("club_pk", models.CharField(max_length=100)),
                ("branch_pk", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Rejected", "Rejected"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("request_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
