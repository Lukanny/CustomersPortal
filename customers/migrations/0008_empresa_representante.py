# Generated by Django 5.0.4 on 2024-06-10 05:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0007_remove_cliente_usuário_da_empresa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_fantasia_da_empresa', models.CharField(max_length=254)),
                ('endereço_da_empresa', models.CharField(max_length=254)),
                ('número_de_telefone_da_empresa', models.CharField(max_length=15)),
                ('email_da_empresa', models.EmailField(max_length=254)),
                ('data_de_registro_da_empresa', models.DateTimeField(editable=False)),
                ('última_edição_no_perfil_da_empresa', models.DateTimeField(editable=False)),
                ('usuários_associados', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=254), blank=True, default=list, size=3)),
            ],
        ),
        migrations.CreateModel(
            name='Representante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_do_representante_legal', models.CharField(max_length=254)),
                ('rg_do_representante_legal', models.CharField(max_length=9)),
                ('cpf_do_representante_legal', models.CharField(max_length=11)),
                ('cargo_do_representante_legal', models.CharField(max_length=254)),
                ('data_de_registro_do_representante', models.DateTimeField(editable=False)),
                ('última_edição_no_perfil_do_representante', models.DateTimeField(editable=False)),
            ],
        ),
    ]
