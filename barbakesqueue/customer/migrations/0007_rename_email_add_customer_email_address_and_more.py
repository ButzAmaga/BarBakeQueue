# Generated by Django 5.1.5 on 2025-03-07 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_customer_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='email_add',
            new_name='email_address',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='contact_num',
        ),
    ]
