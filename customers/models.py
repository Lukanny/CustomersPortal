from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Empresa(models.Model):
    nome_fantasia_da_empresa = models.CharField(max_length=254)
    endereço_da_empresa = models.CharField(max_length=254)
    número_de_telefone_da_empresa = models.CharField(max_length=15)
    cnpj_da_empresa = models.CharField(max_length=12)
    data_de_registro_da_empresa = models.DateTimeField(editable=False)
    última_edição_no_perfil_da_empresa = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_de_registro_da_empresa = timezone.now()
        self.última_edição_no_perfil_da_empresa = timezone.now()
        return super(Empresa, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome_fantasia_da_empresa}"
    

class Representante(models.Model):
    nome_do_representante_legal = models.CharField(max_length=254)
    cpf_do_representante_legal = models.CharField(max_length=11)
    cargo_do_representante_legal = models.CharField(max_length=254)
    email_do_representante_legal = models.EmailField(max_length=254)
    data_de_registro_do_representante = models.DateTimeField(editable=False)
    última_edição_no_perfil_do_representante = models.DateTimeField(editable=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='workers')
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.data_de_registro_do_representante = timezone.now()
        self.última_edição_no_perfil_do_representante = timezone.now()
        return super(Representante, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome_do_representante_legal}"
    