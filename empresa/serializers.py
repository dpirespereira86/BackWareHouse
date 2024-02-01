from rest_framework import serializers
from .models import Empresa, Filial, Fornecedor


class FilialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields=('matriz','razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial','numero_empresa')

class EmpresaSerializers(serializers.ModelSerializer):
    filiais = FilialSerializers(many=True)
    class Meta:
        model = Empresa
        fields=('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','filiais')


class EmpresaCreatedSerializers(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields=('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial',)


class FornecedorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = (
    'id',
    'razao_social',
    'cnpj',
    'endereco',
    'numero',
    'bairro',
    'cidade',
    'uf',
    'telefone',
    'contato',
    'email_responsavel',
    'telefone_responsavel',
    'empresa',
)

