from django.contrib import admin

# Register models .
from Armazem.models import Unidade,Posicao,MOVIMENTACAO,Item,Estoque


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
