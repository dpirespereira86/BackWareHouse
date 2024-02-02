# Generated by Django 5.0.1 on 2024-02-02 14:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0004_alter_pedidocompra_operador'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='aprovacaosolicitacao',
            name='justificativa',
            field=models.TextField(blank=True, null=True, verbose_name='Observação'),
        ),
        migrations.AlterUniqueTogether(
            name='aprovacaosolicitacao',
            unique_together={('usuario', 'solicitacao')},
        ),
    ]