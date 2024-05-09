from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome_do_representante_legal = models.CharField(max_length=254)
    rg_do_representante_legal = models.CharField(max_length=9)
    cpf_do_representante_legal = models.CharField(max_length=11)
    cargo_do_representante_legal = models.CharField(max_length=254)
    nome_fantasia_da_empresa = models.CharField(max_length=254)
    endereço_da_empresa = models.CharField(max_length=254)
    número_de_telefone_da_empresa = models.CharField(max_length=15)
    email_da_empresa = models.EmailField(max_length=254)
    data_de_registro_da_empresa = models.DateTimeField(editable=False)
    última_edição_no_perfil_da_empresa = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.data_de_registro_da_empresa = timezone.now()
        self.última_edição_no_perfil_da_empresa = timezone.now()
        return super(Cliente, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nome_fantasia_da_empresa}"
    

