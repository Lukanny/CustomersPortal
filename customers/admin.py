from django.contrib import admin

from .models import Empresa, Representante

admin.site.register(Empresa)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ['nome_fantasia_da_empresa'] 
    list_display = ('nome_fantasia_da_empresa', 'endereço_da_empresa', 'número_de_telefone_da_empresa', 'cnpj_da_empresa') 
    list_filter = ('data_de_registro_da_empresa',)
    ordering = ('nome_fantasia_da_empresa',)
