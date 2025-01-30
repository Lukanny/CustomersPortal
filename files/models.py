from calendar import monthrange
from customers.models import Empresa
from django.db import models
from django.utils import timezone

def file_upload_path(instance, filename):
    return "/".join([instance.cliente.nome_fantasia, str(instance.data_upload.year), filename])


class Arquivo(models.Model):
    cliente = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='files')
    nome = models.CharField(max_length=255)  # Shortened field name
    descricao = models.TextField(blank=True)  # Shortened field name
    endereco = models.FileField(upload_to=file_upload_path)  # Changed from 'endereço_do_arquivo'
    data_upload = models.DateTimeField(editable=False)  # Changed from 'data_de_upload_do_arquivo'
    ano = models.CharField(max_length=4)  # Changed from 'ano_do_arquivo'
    validade = models.DateField()  # Stores expiration date (last day of the month)

    def __str__(self):
        return f"{self.nome} - {self.data_upload.year} - Cliente: {self.cliente}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_upload = timezone.now()

        # If a user selects only the month and year, default to the last day of the month
        if self.validade:
            year = self.validade.year
            month = self.validade.month
            last_day = monthrange(year, month)[1]  # Get the last day of the month
            self.validade = timezone.datetime(year, month, last_day).date()

        super().save(*args, **kwargs)

        