from django.contrib import admin
from .models import Solicitacao, PedidoCompra, ItemPedidoCompra, ItemSolicitacao, Cotacao


# Register your models here.
@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id','operador','solicitante','observacao','imagem','empresa',)



@admin.register(PedidoCompra)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','operador','solicitante','observacao','imagem','empresa','estimativa_valor','valor_pedido',
    'prazo_de_entrega', 'criacao','atualizacao')

@admin.register(ItemPedidoCompra)
class ItemPedidoCompraAdmin(admin.ModelAdmin):
    list_display = ('id',
    'pedido_compra',
    'codigo',
    'codigo_interno',
    'descricao',
    'quantidade',
    'prazo_de_entrega',
    'valor_unitario',
    'valor_total',)




@admin.register(ItemSolicitacao)
class ItemSolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id','solicitacao','codigo','codigo_interno','descricao','quantidade','criacao',
                    'atualizacao')

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ( 'id','operador','pedido_compra','fornecedor','contato','email_contato','observacao',
    'empresa','valor_pedido','prazo_de_entrega','orcamento','justificativa','fechado')

    