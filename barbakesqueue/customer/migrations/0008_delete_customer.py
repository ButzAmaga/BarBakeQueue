# Generated by Django 5.1.5 on 2025-03-07 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_rename_email_add_customer_email_address_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='customer',
        ),
    ]
