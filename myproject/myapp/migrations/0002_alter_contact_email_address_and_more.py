# Generated by Django 5.1.5 on 2025-01-31 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="email_address",
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="contact",
            name="postcode",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
