from customers.models import Cliente
from django.db import models

import os

def file_upload_path(instance, filename):
    nome_da_empresa = instance.cliente.nome_fantasia_da_empresa
    year = instance.file_uploaded_at.year
    return os.path.join(filename, str(year), nome_da_empresa)


class Arquivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome_do_arquivo = models.CharField(max_length=255)
    descrição_do_arquivo = models.TextField(blank=True)
    endereço_do_arquivo = models.FileField(upload_to=file_upload_path)
    data_de_upload_do_arquivo = models.DateTimeField(editable=False)

    def __str__(self):
        return f"{self.nome_do_arquivo}"
    