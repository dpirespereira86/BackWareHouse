from django.contrib import admin

# Register your models here.
from Produto.models import Produto, Familia, Embalagem


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id','codigo','codigo_Auxiliar','descricao','familia','unidade','tipo_item','ativo','especificacao',
    'peso','observacao','comprimento','largura','altura','imagem','tempo_validade',
    'comprimento','largura','altura','prazo_frete_medio','peso','saldo','estoque_minimo','estoque_maximo',
    'estoque_seguranca','auto_solicitacao','empresa','volume','negativo','alto_valor','pesados','blocados','miudezas',
    'refrigerados','controlados','ultimo_preco','preco_medio',)


@admin.register(Familia)
class FamiliaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Embalagem)
class EmbalagemAdmin(admin.ModelAdmin):
    list_display = ('produto',
    'descricao',
    'codigo',
    'comprimento',
    'largura',
    'altura',
    'quantidade_produto',
    'volume',
    'tipo',
    'empresa',)


