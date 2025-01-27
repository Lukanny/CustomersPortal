from django.contrib import admin
from .models import Arquivo

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nome_do_arquivo', 'ano_do_arquivo', 'data_de_upload_do_arquivo')
    list_filter = ('ano_do_arquivo',)
    search_fields = ('nome_do_arquivo', 'cliente__nome_fantasia_da_empresa')
    ordering = ('cliente', 'ano_do_arquivo', 'nome_do_arquivo')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('cliente')  # Melhora a performance carregando o cliente junto
