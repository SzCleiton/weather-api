from django.contrib import admin
from .models import SearchHistory

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """
    Configura a exibição do modelo SearchHistory na interface de admin.
    """
    list_display = ('city', 'user', 'timestamp') # Colunas a serem exibidas na lista
    list_filter = ('timestamp', 'city') # Adiciona filtros na barra lateral
    search_fields = ('city', 'user__username') # Adiciona um campo de busca
    readonly_fields = ('city', 'user', 'request_data', 'timestamp') # Campos que não podem ser editados no admin

    # Impede a criação de novos registros pelo admin, pois eles devem vir da API
    def has_add_permission(self, request):
        return False

    # Impede a exclusão pelo admin, para manter o histórico fiel
    def has_delete_permission(self, request, obj=None):
        return False