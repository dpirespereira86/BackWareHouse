from rest_framework import serializers
from .models import Unidade,MOVIMENTACAO,Estoque,Item,Posicao,Conferencia,ItensConferencia,Transitorio

class UnidadeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Unidade
        fields=('nome','empresa')


class EstoqueProdutoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields=( 'posicao','quantidade','empresa')


class EstoqueSerializers(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields=( 'posicao','produto','quantidade','empresa')

class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields=( 'id','codigo','codigo_interno','descricao','quantidade','movimentacao','empresa')

class PosicaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posicao
        fields=('id','unidade','nome','rua','predio','nivel','sequencia','peso','capacidade','volume','empresa')

class MovimentacaoSerializers(serializers.ModelSerializer):
    class Meta:
        model = MOVIMENTACAO
        fields=('id','tipo','date','operador','posicao','empresa')

class MovimentacaoItemSerializers(serializers.ModelSerializer):
    itens = ItemSerializers(many=True)
    class Meta:
        model = MOVIMENTACAO
        fields=('id','tipo','date','operador','posicao','tipo_conferencia','empresa','itens')

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        movimentacao = MOVIMENTACAO.objects.create(**validated_data)
        for itens_data in itens_data:
            Item.objects.create(movimentacao=movimentacao, **itens_data)
        return movimentacao

class AprovacaoMovimentacaoItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = MOVIMENTACAO
        fields=('id','aprovado')


class ItemConferenciaSerializers(serializers.ModelSerializer):
    class Meta:
        model = ItensConferencia
        fields=(
    'conferencia',
    'id',
    'codigo',
    'quantidade',
                )
class ConferenciaSerializers(serializers.ModelSerializer):
    itens_conferencias = ItemConferenciaSerializers(many=True)
    class Meta:
        model = Conferencia
        fields=( 'id',
                 'tipo_conferencia',
                  'operador',
                  'empresa',
                  'pedido',
                  'nf',
                  'fluxo',
                  'itens_conferencias',
    )

    def create(self, validated_data):
        itens_conferencias = validated_data.pop('itens_conferencias')
        conferencia= Conferencia.objects.create(**validated_data)
        for itens_conferencias in itens_conferencias:
            ItensConferencia.objects.create(conferencia=conferencia, **itens_conferencias)
        print(conferencia)
        return conferencia

class TransitorioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transitorio
        fields=('id'
        'codigo' 
        'codigo_interno'
        'descricao'
        'quantidade'
        'conferencia'
        'empresa'
        'status')
