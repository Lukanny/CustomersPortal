# Generated by Django 5.0.4 on 2024-05-08 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_worker_name', models.CharField(max_length=254)),
                ('company_worker_id', models.CharField(max_length=9)),
                ('company_worker_nif', models.CharField(max_length=11)),
                ('company_worker_position', models.CharField(max_length=254)),
                ('company_name', models.CharField(max_length=254)),
                ('company_address', models.CharField(max_length=254)),
                ('company_number', models.CharField(max_length=15)),
                ('company_email', models.EmailField(max_length=254)),
                ('company_registered_at', models.DateTimeField(editable=False)),
                ('company_last_edition', models.DateTimeField()),
            ],
        ),
    ]
