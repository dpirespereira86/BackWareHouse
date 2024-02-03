from django.contrib import admin
from .models import Configuracao,Aprovacao_Config

# Register your models here.
@admin.register(Configuracao)
class ConfigAdmin(admin.ModelAdmin):
    list_display = (
    'empresa',
    'geracao_pedido_auto',
    )

@admin.register(Aprovacao_Config)
class AprovacaoConfigAdmin(admin.ModelAdmin):
    list_display = (
        'pessoa',
        'nivel',
        'configuracao'
    )