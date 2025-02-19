from django.contrib import admin
from .models import Arquivo

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'nome', 'ano', 'data_upload')
    list_filter = ('ano',)
    search_fields = ('nome', 'cliente__nome_fantasia')
    ordering = ('cliente', 'ano', 'nome')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('cliente')
