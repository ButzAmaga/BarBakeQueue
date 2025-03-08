# Generated by Django 5.1.5 on 2025-03-08 04:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cake', '0009_alter_cake_rating'),
        ('customer', '0010_alter_customer_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('cake', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake.cake')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='customer.customer')),
            ],
        ),
    ]
