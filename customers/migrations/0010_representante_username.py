# Generated by Django 5.0.4 on 2024-06-10 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0009_delete_cliente_representante_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='representante',
            name='username',
            field=models.CharField(default='abc', max_length=254),
            preserve_default=False,
        ),
    ]