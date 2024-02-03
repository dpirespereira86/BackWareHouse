# Generated by Django 5.0.1 on 2024-02-01 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Pedido', '0001_initial'),
        ('Produto', '0001_initial'),
        ('empresa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='aprovacaosolicitacao',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprovacoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuarios'),
        ),
        migrations.AddField(
            model_name='cotacao',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cotações', to='empresa.empresa'),
        ),
        migrations.AddField(
            model_name='itemcotacao',
            name='codigo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='Produto.produto'),
        ),
        migrations.AddField(
            model_name='itemcotacao',
            name='cotacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='Pedido.cotacao'),
        ),
        migrations.AddField(
            model_name='itemcotacao',
            name='fornecedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='empresa.fornecedor'),
        ),
        migrations.AddField(
            model_name='itempedidocompra',
            name='codigo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_compra', to='Produto.produto'),
        ),
        migrations.AddField(
            model_name='itempedidocompra',
            name='fornecedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_compra', to='empresa.fornecedor'),
        ),
        migrations.AddField(
            model_name='itemsolicitacao',
            name='codigo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_solicitacoes', to='Produto.produto'),
        ),
        migrations.AddField(
            model_name='pedidocompra',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_compras', to='empresa.empresa'),
        ),
        migrations.AddField(
            model_name='itempedidocompra',
            name='pedido_compra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_compra', to='Pedido.pedidocompra'),
        ),
        migrations.AddField(
            model_name='itemavulsopedido',
            name='pedido_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_avulso', to='Pedido.pedidocompra'),
        ),
        migrations.AddField(
            model_name='cotacao',
            name='pedido_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cotacoes', to='Pedido.pedidocompra'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes', to='empresa.empresa'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solictacoes_de_compra', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='itemsolicitacao',
            name='solicitacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itens_solicitacoes', to='Pedido.solicitacao'),
        ),
        migrations.AddField(
            model_name='itemavulso',
            name='solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_avulso', to='Pedido.solicitacao'),
        ),
        migrations.AddField(
            model_name='aprovacaosolicitacao',
            name='solicitacao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_solictacao', to='Pedido.solicitacao'),
        ),
        migrations.AlterUniqueTogether(
            name='pedidocompra',
            unique_together={('id', 'empresa')},
        ),
        migrations.AlterUniqueTogether(
            name='solicitacao',
            unique_together={('id', 'empresa')},
        ),
    ]
