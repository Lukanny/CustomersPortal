# Generated by Django 5.0.4 on 2024-06-10 05:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_alter_cliente_usuário_da_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='usuário_da_empresa',
        ),
        migrations.AddField(
            model_name='cliente',
            name='usuários_da_empresa',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=['abc', 'abcde'], size=10),
            preserve_default=False,
        ),
    ]
