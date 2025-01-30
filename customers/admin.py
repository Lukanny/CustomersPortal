from django.contrib import admin
from .models import Empresa
from files.models import Arquivo

class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 0
    fields = ('nome', 'ano', 'endereco')
    readonly_fields = ('ano', 'endereco')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'cnpj', 'telefone')
    search_fields = ('nome_fantasia', 'cnpj')
    inlines = [ArquivoInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('files')  # Carrega arquivos relacionados para performance
