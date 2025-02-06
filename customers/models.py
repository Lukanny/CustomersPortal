from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Endereco(models.Model):
    rua = models.CharField(max_length=254)
    bairro = models.CharField(max_length=254)
    numero = models.CharField(max_length=10)  # Changed from 'número'
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=100, default="Brasil")  # Changed from 'país'

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - {self.estado} ({self.cep})"


class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=254)  # Shortened field name
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, related_name="empresa")  # Changed from 'endereço_da_empresa'
    telefone = models.CharField(max_length=15)  # Shortened field name
    cnpj = models.CharField(max_length=14)
    data_registro = models.DateTimeField(editable=False)  # Changed from 'data_de_registro_da_empresa'
    ultima_edicao = models.DateTimeField(editable=False)  # Changed from 'última_edição_no_perfil_da_empresa'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_registro = timezone.now()
        self.ultima_edicao = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_fantasia
 

class Representante(models.Model):
    nome = models.CharField(max_length=254)  # Shortened field name
    cpf = models.CharField(max_length=11)  # Shortened field name
    cargo = models.CharField(max_length=254)  # Shortened field name
    email = models.EmailField(max_length=254)
    data_registro = models.DateTimeField(editable=False)  # Changed from 'data_de_registro_do_representante'
    ultima_edicao = models.DateTimeField(editable=False)  # Changed from 'última_edição_no_perfil_do_representante'
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='workers')
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def cnpj(self):
        return self.empresa.cnpj if self.empresa else None  # Changed from 'cnpj_da_empresa'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_registro = timezone.now()
        self.ultima_edicao = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    