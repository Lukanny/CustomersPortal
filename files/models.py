from calendar import monthrange
from customers.models import Empresa
from django.db import models
from django.utils import timezone

def file_upload_path(instance, filename):
    return "/".join([instance.cliente.nome_fantasia_da_empresa, str(instance.data_de_upload_do_arquivo.year), filename])


class Arquivo(models.Model):
    cliente = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='files')
    nome_do_arquivo = models.CharField(max_length=255)
    descrição_do_arquivo = models.TextField(blank=True)
    endereço_do_arquivo = models.FileField(upload_to=file_upload_path)
    data_de_upload_do_arquivo = models.DateTimeField(editable=False)
    ano_do_arquivo = models.CharField(max_length=4)
    validade_do_arquivo = models.DateField()  # Stores expiration date (last day of the month)

    def __str__(self):
        return f"{self.nome_do_arquivo} - {self.data_de_upload_do_arquivo.year} - Cliente: {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_de_upload_do_arquivo = timezone.now()

        # If a user selects only the month and year, default to the last day of the month
        if self.validade_do_arquivo:
            year = self.validade_do_arquivo.year
            month = self.validade_do_arquivo.month
            last_day = monthrange(year, month)[1]  # Get the last day of the month
            self.validade_do_arquivo = timezone.datetime(year, month, last_day).date()

        return super(Arquivo, self).save(*args, **kwargs)

        