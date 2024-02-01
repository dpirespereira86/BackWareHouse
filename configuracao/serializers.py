from .models import Configuracao,Aprovacao_Config
from rest_framework import serializers


class AprovConfigSerializers(serializers.ModelSerializer):
    class Meta:
        model = Aprovacao_Config
        fields=(
        'pessoa',
        'nivel',
        )
class ConfigSerializers(serializers.ModelSerializer):
    pessoas = AprovConfigSerializers(many=True)
    class Meta:
        model = Configuracao
        fields=(
    'id',
    'empresa',
    'pessoa',
    'geracao_pedido_auto',
    'pessoas'
    )

    def create(self, validated_data):
        pessoas_data = validated_data.pop('pessoas')
        configuracoes = Configuracao.objects.create(**validated_data)
        for pessoas_data in pessoas_data:
            Aprovacao_Config.objects.create(configuracoes=configuracoes, **pessoas_data)
        return configuracoes