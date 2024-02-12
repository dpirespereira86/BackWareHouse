from django.contrib import admin

# Register models .
from Armazem.models import Unidade, Posicao, MOVIMENTACAO, Item, Estoque, Conferencia, Transitorio


@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Posicao)
class PosicaoAdmin(admin.ModelAdmin):
    list_display = ('id','unidade','nome','rua','predio','nivel','sequencia')

@admin.register(MOVIMENTACAO)
class MOVIMENTACAOAdmin(admin.ModelAdmin):
    list_display = ('id','tipo','date','operador','posicao')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ( 'id','codigo','codigo_interno','descricao','quantidade',)

@admin.register(Estoque)
class EstoqueAdmin(admin.ModelAdmin):
    list_display = ('posicao','produto','quantidade',)

@admin.register(Conferencia)
class ConferenciaAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'tipo_conferencia',
    'operador',
    'empresa',
    'pedido',
    'nf',
    'fluxo',
    )
@admin.register(Transitorio)
class TransitorioAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'codigo',
    'codigo_interno',
    'descricao',
    'quantidade',
    'conferencia',
    'empresa',
    'aprovado_conferencia',
    'criacao',
    'atualizacao'
    )

