# Generated by Django 5.0.1 on 2024-01-26 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='familia', to='empresa.empresa')),
            ],
            options={
                'verbose_name': 'Familia',
                'db_table': 'Familia',
                'unique_together': {('nome', 'empresa')},
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=30)),
                ('codigo_Auxiliar', models.CharField(blank=True, max_length=30, null=True)),
                ('descricao', models.CharField(max_length=100)),
                ('unidade', models.CharField(choices=[('Cj', 'Conjunto'), ('Cx', 'Caixa'), ('Dz', 'Dúzia'), ('Fd', 'Fardo'), ('Fl', 'Folha'), ('Gl', 'Galão'), ('Lt', 'Lote'), ('Jg', 'Jogo'), ('Kg', 'Kilograma'), ('L', 'Litro'), ('Lta', 'Lata'), ('M', 'Metro'), ('Mil', 'Milheiro'), ('Par', 'Par'), ('Pct', 'Pacote'), ('Pç', 'Peça'), ('Res', 'Resma'), ('Rl', 'Rolo'), ('Ton', 'Tonelada'), ('Und', 'Unidade'), ('Vd', 'Vidro'), ('M³', 'Metro_cubico'), ('M²', 'Metro_quadrado')], max_length=30)),
                ('tipo_item', models.CharField(choices=[('1', 'Matéria-prima'), ('2', 'Bens para varejo'), ('3', 'Consumo interno da organização'), ('4', 'Estoque de segurança')], max_length=60)),
                ('ativo', models.BooleanField(default=True)),
                ('especificacao', models.TextField(blank=True, max_length=200, null=True)),
                ('observacao', models.TextField(blank=True, max_length=200, null=True)),
                ('imagem', models.ImageField(blank=True, default='', null=True, upload_to='')),
                ('tempo_validade', models.IntegerField(default=0)),
                ('comprimento', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('largura', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('altura', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('prazo_frete_medio', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('peso', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('estoque_minimo', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('estoque_maximo', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('estoque_seguranca', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('auto_solicitacao', models.BooleanField(default=False)),
                ('volume', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('negativo', models.BooleanField(default=True)),
                ('alto_valor', models.BooleanField(default=False)),
                ('pesados', models.BooleanField(default=False)),
                ('blocados', models.BooleanField(default=False)),
                ('miudezas', models.BooleanField(default=False)),
                ('refrigerados', models.BooleanField(default=False)),
                ('controlados', models.BooleanField(default=False)),
                ('ultimo_preco', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('preco_medio', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='empresa.empresa')),
                ('familia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='Produto.familia')),
                ('fornecedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='empresa.fornecedor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'Produto',
                'unique_together': {('codigo', 'empresa')},
            },
        ),
        migrations.CreateModel(
            name='Embalagem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=30)),
                ('comprimento', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('largura', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('altura', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('quantidade_produto', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('volume', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('tipo', models.CharField(max_length=100)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embalagens', to='empresa.empresa')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='embalagens', to='Produto.produto')),
            ],
            options={
                'verbose_name': 'Embalagem',
                'verbose_name_plural': 'Embalagens',
                'db_table': 'Embalagem',
            },
        ),
    ]
