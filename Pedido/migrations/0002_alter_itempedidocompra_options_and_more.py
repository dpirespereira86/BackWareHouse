# Generated by Django 5.0.1 on 2024-01-29 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedido', '0001_initial'),
        ('Produto', '0001_initial'),
        ('empresa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itempedidocompra',
            options={'verbose_name': 'Item Pedido de Compra', 'verbose_name_plural': 'Itens Pedido de Compra'},
        ),
        migrations.AlterModelOptions(
            name='pedidocompra',
            options={'verbose_name': 'Pedido de Compra', 'verbose_name_plural': 'Pedidos de Compra'},
        ),
        migrations.RemoveField(
            model_name='cotacao',
            name='atualizacao',
        ),
        migrations.RemoveField(
            model_name='solicitacao',
            name='atualizacao',
        ),
        migrations.AddField(
            model_name='cotacao',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AddField(
            model_name='itempedidocompra',
            name='fornecedor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_compra', to='empresa.fornecedor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itempedidocompra',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AddField(
            model_name='itemsolicitacao',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AddField(
            model_name='itemsolicitacao',
            name='total_estimado',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemsolicitacao',
            name='ultimo_preco_unit',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedidocompra',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='descricao',
            field=models.TextField(default=1, verbose_name='observação'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='justificativa',
            field=models.TextField(blank=True, null=True, verbose_name='justificativa'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='modificado',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualização'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='urgencia',
            field=models.BooleanField(default=False, verbose_name='Urgente'),
        ),
        migrations.AddField(
            model_name='solicitacao',
            name='valor_estimado',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='cotacao',
            name='criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data Criação'),
        ),
        migrations.AlterField(
            model_name='cotacao',
            name='orcamento',
            field=models.FileField(blank=True, null=True, upload_to='orcamento/'),
        ),
        migrations.AlterField(
            model_name='itemsolicitacao',
            name='criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data Criação'),
        ),
        migrations.AlterField(
            model_name='pedidocompra',
            name='nf',
            field=models.FileField(blank=True, null=True, upload_to='nf/'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data Criação'),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='solicitante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solictacoes_de_compra', to=settings.AUTH_USER_MODEL, verbose_name='Solicitante'),
        ),
        migrations.CreateModel(
            name='AprovacaoSolicitacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('justificativa', models.TextField(verbose_name='Observação')),
                ('aprovado', models.BooleanField(default=False, verbose_name='Aprovado')),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_solictacao', to='Pedido.solicitacao')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprovacoes', to=settings.AUTH_USER_MODEL, verbose_name='Usuarios')),
            ],
            options={
                'verbose_name': 'Aprovação de Solicitação',
                'verbose_name_plural': 'Aprovações de Solicitações',
                'db_table': 'Aprovacao_Solicitacao_de_Compra',
            },
        ),
        migrations.CreateModel(
            name='ItemAvulso',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.CharField(max_length=100)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('empresa', models.CharField(max_length=30)),
                ('fornecedor_indicado', models.CharField(blank=True, max_length=100, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_Avulso', to='Pedido.solicitacao')),
            ],
            options={
                'verbose_name': 'Item Avulso Solicitação ',
                'verbose_name_plural': 'Itens Avulsos Solictação',
                'db_table': 'Item_Avulso_Solicitacao',
            },
        ),
        migrations.CreateModel(
            name='ItemAvulsoPedido',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('descricao', models.CharField(max_length=100)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('empresa', models.CharField(max_length=30)),
                ('fornecedor_indicado', models.CharField(blank=True, max_length=100, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('solicitacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_pedido_avulso', to='Pedido.solicitacao')),
            ],
            options={
                'verbose_name': 'Item Avulso Pedido ',
                'verbose_name_plural': 'Itens Avulsos Pedido',
                'db_table': 'Item_Avulso_Pedido',
            },
        ),
        migrations.CreateModel(
            name='ItemCotacao',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data Criação')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Atualização')),
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('codigo_interno', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=100)),
                ('quantidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('empresa', models.CharField(max_length=30)),
                ('ultimo_preco', models.DecimalField(decimal_places=2, max_digits=5)),
                ('valor_unit', models.DecimalField(decimal_places=2, max_digits=5)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('codigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='Produto.produto')),
                ('cotacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='Pedido.cotacao')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_cotacoes', to='empresa.fornecedor')),
            ],
            options={
                'verbose_name': 'Item_cotacao',
                'verbose_name_plural': 'Itens_cotacao',
                'db_table': 'Item_cotacao',
            },
        ),
    ]
