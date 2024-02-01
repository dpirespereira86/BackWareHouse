from rest_framework import serializers
from .models import Produto,Familia
from Armazem.serializers import EstoqueProdutoSerializers



class ProdutoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields=('id','codigo','codigo_Auxiliar','descricao','familia','unidade','tipo_item','ativo','especificacao',
    'prazo_frete_medio','peso','observacao','comprimento','largura','altura','imagem','empresa','fornecedor')

class ProdutoEstoqueSerializers(serializers.ModelSerializer):
    estoques= EstoqueProdutoSerializers(many=True)
    class Meta:
        model = Produto
        fields=('id','codigo','saldo','estoques')

class FamiliaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Familia
        fields = ('nome','empresa')