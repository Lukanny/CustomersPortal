from customers.models import Cliente
from django.db import models
from django.utils import timezone

def file_upload_path(instance, filename):
    return "/".join([instance.cliente.nome_fantasia_da_empresa, str(instance.data_de_upload_do_arquivo.year), filename])


class Arquivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    nome_do_arquivo = models.CharField(max_length=255)
    descrição_do_arquivo = models.TextField(blank=True)
    endereço_do_arquivo = models.FileField(upload_to=file_upload_path)
    data_de_upload_do_arquivo = models.DateTimeField(editable=False)

    def __str__(self):
        return f"{self.nome_do_arquivo} - {self.data_de_upload_do_arquivo.year} - Cliente: {self.cliente}"

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.data_de_upload_do_arquivo = timezone.now()
        return super(Arquivo, self).save(*args, **kwargs)
    