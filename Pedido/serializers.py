from rest_framework import serializers
from .models import (Solicitacao,PedidoCompra,ItemPedidoCompra,ItemSolicitacao,Cotacao,ItemCotacao,ItemAvulso,
                     ItemAvulsoPedido,AprovacaoSolicitacao)

######################################### Solicitações #################################################################
class ItemSolicitacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemSolicitacao
        fields=('id','solicitacao','codigo','descricao','quantidade',)



class ItemAvulsoSerializers(serializers.ModelSerializer):

    class Meta:
        model =ItemAvulso
        fields=('id',
                'descricao',
                'quantidade',
                'imagem',
                'fornecedor_indicado',
                'total',
        )


class SolictacaoSerializers(serializers.ModelSerializer):
    itens_solicitacoes = ItemSolicitacaoSerializers(many=True)
    itens_avulso = ItemAvulsoSerializers(many=True)
    class Meta:
        model = Solicitacao
        fields = (
        'solicitante',
        'observacao',
        'urgencia',
        'justificativa',
        'empresa',
        'valor_estimado',
        'descricao',
        'itens_solicitacoes',
        'itens_avulso'
        )


    def create(self, validated_data):
        itens_data = validated_data.pop('itens_solicitacoes')
        itens_avulso = validated_data.pop('itens_avulso')
        solicitacao = Solicitacao.objects.create(**validated_data)
        for itens_data in itens_data:
            ItemSolicitacao.objects.create(solicitacao=solicitacao, **itens_data)
        for itens_avulso in itens_avulso:
            ItemAvulso.objects.create(solicitacao=solicitacao, **itens_avulso)
        return solicitacao

########################################################################################################################

################################################ Orçamento #############################################################
class ItemCotacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemCotacao
        fields=(
        'id',
        'cotacao',
        'codigo',
        'codigo_interno',
        'descricao',
        'quantidade',
        'empresa',
        'ultimo_preco',
        'valor_unit',
        'total',
        'fornecedor',
        )

class CotacaoSerializers(serializers.ModelSerializer):
    itens_cotacoes = ItemCotacaoSerializers(many=True)
    class Meta:
        model = Cotacao
        fields=(
        'id',
        'operador',
        'pedido_compra',
        'fornecedor',
        'contato',
        'email_contato',
        'observacao',
        'empresa',
        'valor_pedido',
        'prazo_de_entrega',
        'orcamento',
        'justificativa',
        'fechado',
        'fechado',
        'itens_cotacoes'
    )

    def create(self, validated_data):
        itens_cotacoes = validated_data.pop('itens_cotacoes')
        cotacao = Cotacao.objects.create(**validated_data)
        for itens_cotacoes in itens_cotacoes:
            ItemCotacao.objects.create(cotacao=cotacao, **itens_cotacoes)
        return cotacao


########################################################################################################################

######################################### Pedido de Compra #############################################################

class ItemPedidoCompraSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemPedidoCompra
        fields=('id','pedido_compra','codigo','descricao','quantidade','valor_unitario','valor_total','fornecedor')

class ItemAvulsoPedidoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemAvulsoPedido
        fields=('id','pedido_compra','codigo','codigo_interno','descricao','quantidade',)
class PedidoCompraSerializers(serializers.ModelSerializer):
    itens_pedido_compra = ItemPedidoCompraSerializers(many=True)
    itens_pedido_avulso = ItemAvulsoPedidoSerializers(many=True)
    cotacoes = CotacaoSerializers(many=True)
    class Meta:
        model = PedidoCompra
        fields=('id','operador','solicitante','observacao','imagem','empresa','estimativa_valor','valor_pedido',
    'prazo_de_entrega','itens_pedido_compra','itens_pedido_avulso','cotacoes' )

    def create(self, validated_data):

        itens_compra = validated_data.pop('itens_pedido_compra')
        itens_avulso_compra = validated_data.pop('itens_pedido_avulso')
        cotacoes_data = validated_data.pop('cotacoes')
        pedido_compra = PedidoCompra.objects.create(**validated_data)


        for itens_compra  in itens_compra :
            ItemPedidoCompra.objects.create(pedido_compra=pedido_compra, **itens_compra )

        for itens_avulso_compra  in itens_avulso_compra :
            ItemAvulsoPedido.objects.create(pedido_compra=pedido_compra, **itens_avulso_compra )

        for cotacoes_data in cotacoes_data:
            Cotacao.objects.create(pedido_compra=pedido_compra, **cotacoes_data)

        return pedido_compra

########################################################################################################################

####################################################### Aprovacao ######################################################
class AprovacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = AprovacaoSolicitacao
        fields=(
            'id',
            'usuario',
            'justificativa',
            'aprovado',
            'solicitacao',
        )

class SolicitacaoSemAprovacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Solicitacao
        fields = (
        'id',
        'solicitante',
        'observacao',
        'urgencia',
        'descricao',
        )



