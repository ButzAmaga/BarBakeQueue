# Generated by Django 5.1.5 on 2025-03-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0004_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('init_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone_num', models.CharField(max_length=11)),
                ('home_address', models.CharField(default='Daraga', max_length=100)),
                ('email_add', models.EmailField(max_length=254)),
                ('contact_num', models.IntegerField(default='09123456789')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='Customer/Profile Picture')),
            ],
        ),
    ]
