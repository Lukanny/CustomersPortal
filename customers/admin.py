from django.contrib import admin
from .models import Empresa
from files.models import Arquivo

class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 0
    fields = ('nome_do_arquivo', 'ano_do_arquivo', 'endereço_do_arquivo')
    readonly_fields = ('ano_do_arquivo', 'endereço_do_arquivo')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia_da_empresa', 'cnpj_da_empresa', 'número_de_telefone_da_empresa')
    search_fields = ('nome_fantasia_da_empresa', 'cnpj_da_empresa')
    inlines = [ArquivoInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('files')  # Carrega arquivos relacionados para performance
