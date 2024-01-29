from rest_framework import serializers
from .models import Empresa,Filial




class FilialSerializers(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields=('matriz','razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial','data_cadastro','numero_empresa')

class EmpresaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        filiais = FilialSerializers(many=True)
        fields=('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial','data_cadastro','filiais')