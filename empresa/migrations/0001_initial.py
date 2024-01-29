# Generated by Django 5.0.1 on 2024-01-26 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('razao_social', models.CharField(max_length=30, unique=True)),
                ('cnpj', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('endereco', models.CharField(max_length=100)),
                ('numero', models.IntegerField(default=0)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('uf', models.CharField(max_length=2)),
                ('telefone', models.CharField(max_length=10)),
                ('first_name_responsavel', models.CharField(max_length=50)),
                ('last_name_responsavel', models.CharField(max_length=50)),
                ('email_responsavel', models.EmailField(max_length=254)),
                ('telefone_responsavel', models.CharField(max_length=10)),
                ('wms', models.BooleanField(default=False)),
                ('compras', models.BooleanField(default=False)),
                ('frota', models.BooleanField(default=False)),
                ('ativo', models.BooleanField(default=False)),
                ('senha_inicial', models.CharField(max_length=8)),
                ('data_cadastro', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('razao_social', models.CharField(max_length=30, unique=True)),
                ('cnpj', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('endereco', models.CharField(max_length=100)),
                ('numero', models.IntegerField(default=0)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('uf', models.CharField(max_length=2)),
                ('telefone', models.CharField(max_length=10)),
                ('contato', models.CharField(max_length=150)),
                ('email_responsavel', models.EmailField(max_length=254)),
                ('telefone_responsavel', models.CharField(max_length=10)),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fornecedores', to='empresa.empresa')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'db_table': 'Fornecedores',
            },
        ),
        migrations.CreateModel(
            name='Filial',
            fields=[
                ('empresa_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='empresa.empresa')),
                ('numero_empresa', models.CharField(blank=True, default='', max_length=30, null=True)),
                ('matriz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filiais', to='empresa.empresa')),
            ],
            options={
                'verbose_name': 'Filial',
                'verbose_name_plural': 'Filiais',
            },
            bases=('empresa.empresa',),
        ),
    ]
