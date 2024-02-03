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
    aprovacoes_config = AprovConfigSerializers(many=True)
    class Meta:
        model = Configuracao
        fields=(

    'empresa',
    'geracao_pedido_auto',
    'aprovacoes_config'
    )

    def create(self, validated_data):
        aprovacoes_data = validated_data.pop('aprovacoes_config')
        configuracao = Configuracao.objects.create(**validated_data)
        for aprovacoes_data in aprovacoes_data:
            Aprovacao_Config.objects.create(configuracao=configuracao, **aprovacoes_data)
        return configuracao