# Generated by Django 5.1.5 on 2025-03-03 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cake', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='availability',
            field=models.CharField(choices=[('available', 'Available'), ('not_available', 'Not Available')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cake',
            name='group_by',
            field=models.CharField(choices=[('birthday', 'Birthday'), ('wedding', 'Wedding'), ('anniversary', 'Anniversary'), ('monthsary', 'Monthsary'), ('christening', 'Christening'), ('debut', 'Debut'), ('gender_reveal', 'Gender Reveal'), ('christmas', 'Christmas'), ('new_year', 'New Year')], max_length=20),
        ),
        migrations.AlterField(
            model_name='cake_image',
            name='image',
            field=models.ImageField(upload_to='Cakes'),
        ),
        migrations.CreateModel(
            name='Shape',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shape', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='Cakes/Shape')),
                ('cake_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cake.cake')),
            ],
        ),
    ]
