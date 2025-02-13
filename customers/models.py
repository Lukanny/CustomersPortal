from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Endereco(models.Model):
    rua = models.CharField(max_length=254)
    bairro = models.CharField(max_length=254)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=9)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    pais = models.CharField(max_length=100, default="Brasil")

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - {self.estado} ({self.cep})"


class Empresa(models.Model):
    nome_fantasia = models.CharField(max_length=254)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, related_name="empresa")
    telefone = models.CharField(max_length=15)
    cnpj = models.CharField(max_length=14)
    data_registro = models.DateTimeField(editable=False)
    ultima_edicao = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_registro = timezone.now()
        self.ultima_edicao = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_fantasia
 

class Representante(models.Model):
    nome = models.CharField(max_length=254)  
    cpf = models.CharField(max_length=11)  
    cargo = models.CharField(max_length=254)  
    email = models.EmailField(max_length=254)
    data_registro = models.DateTimeField(editable=False)  
    ultima_edicao = models.DateTimeField(editable=False)  
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='workers')
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=255, blank=True, null=True) 

    @property
    def cnpj(self):
        return self.empresa.cnpj if self.empresa else None

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_registro = timezone.now()
        self.ultima_edicao = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    