from rest_framework import serializers
from .models import (Solicitacao,PedidoCompra,ItemPedidoCompra,ItemSolicitacao,Cotacao,ItemCotacao,ItemAvulso,
                     ItemAvulsoPedido)


class ItemSolicitacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemSolicitacao
        fields=('id','solicitacao','codigo','descricao','quantidade',)


class ItemPedidoCompraSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemPedidoCompra
        fields=('id','solicitacao','codigo','codigo_interno','descricao','quantidade','empresa',)

class SolictacaoSerializers(serializers.ModelSerializer):
    itens = ItemSolicitacaoSerializers(many=True)
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
        'itens'
        )


        def create(self, validated_data):
            itens_data = validated_data.pop('itens')
            solicitacao = Solicitacao.objects.create(**validated_data)
            for itens_data in itens_data:
                ItemSolicitacao.objects.create(solicitacao=solicitacao, **itens_data)
            return solicitacao

class ItemCotacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItemCotacao
        fields=( 'id',
        'cotacao',
        'codigo',
        'codigo_interno',
        'descricao',
        'quantidade',
        'empresa',
        'ultimo_preco',
        'valor_unit',
        'total',
        'fornecedor', )



class CotacaoSerializers(serializers.ModelSerializer):
    itens_cotacoes = ItemCotacaoSerializers(many=True)
    class Meta:
        model = Cotacao
        fields=('id','operador','pedido_compra','fornecedor','contato','email_contato','observacao',
    'empresa','valor_pedido','prazo_de_entrega','orcamento','justificativa','fechado','itens_cotacoes')

    def create(self, validated_data):
        itens_cotacoes = validated_data.pop('itens_cotacoes')
        cotacao = Cotacao.objects.create(**validated_data)
        for itens_cotacoes in itens_cotacoes:
            ItemCotacao.objects.create(cotacao=cotacao, **itens_cotacoes)
        return cotacao


class PedidoCompraSerializers(serializers.ModelSerializer):
    itens = ItemPedidoCompraSerializers(many=True)
    cotacoes = CotacaoSerializers(many=True)
    class Meta:
        model = PedidoCompra
        fields=('id','operador','solicitante','observacao','imagem','empresa','estimativa_valor','valor_pedido',
    'prazo_de_entrega','itens','cotacoes' )

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        cotacoes_data = validated_data.pop('cotacoes')
        solicitacao = Solicitacao.objects.create(**validated_data)
        for itens_data in itens_data:
            ItemSolicitacao.objects.create(solicitacao=solicitacao, **itens_data)
        for cotacoes_data in cotacoes_data:
            cotacoes_data.objects.create(solicitacao=solicitacao, **cotacoes_data)
        return solicitacao






