from django.contrib import admin
from .models import Solicitacao, PedidoCompra, ItemPedidoCompra, ItemSolicitacao, Cotacao,AprovacaoSolicitacao


# Register your models here.
@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id','solicitante','observacao','empresa',)


@admin.register(PedidoCompra)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id','operador','solicitante','observacao','imagem','empresa','estimativa_valor','valor_pedido',
    'prazo_de_entrega')

@admin.register(ItemPedidoCompra)
class ItemPedidoCompraAdmin(admin.ModelAdmin):
    list_display = ('id',
    'pedido_compra',
    'codigo',
    'descricao',
    'quantidade',
    'prazo_de_entrega',
    'valor_unitario',
    'valor_total',)


@admin.register(ItemSolicitacao)
class ItemSolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('id','solicitacao','codigo','descricao','quantidade','criacao',
                    )

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = ( 'id','operador','pedido_compra','fornecedor','contato','email_contato','observacao',
    'empresa','valor_pedido','prazo_de_entrega','orcamento','justificativa','fechado')


@admin.register(AprovacaoSolicitacao)
class ItemSolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario',
    'justificativa',
    'aprovado',
    'solicitacao',
                    )
