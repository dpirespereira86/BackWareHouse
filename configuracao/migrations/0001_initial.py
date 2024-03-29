# Generated by Django 5.0.1 on 2024-02-02 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresa', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracao',
            fields=[
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('geracao_pedido_auto', models.BooleanField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='configuracoes', to='empresa.empresa')),
            ],
            options={
                'verbose_name': 'Configuração',
                'verbose_name_plural': 'Configurações',
                'db_table': 'Configuracao',
                'unique_together': {('id', 'empresa')},
            },
        ),
        migrations.CreateModel(
            name='Aprovacao_Config',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criacao', models.DateTimeField(auto_now_add=True)),
                ('atualizacao', models.DateTimeField(auto_now_add=True)),
                ('nivel', models.IntegerField()),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprovacoes_config', to=settings.AUTH_USER_MODEL)),
                ('configuracao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aprovacoes_config', to='configuracao.configuracao')),
            ],
            options={
                'verbose_name': 'Aprovacao de Configuração',
                'verbose_name_plural': 'Aprovacões de Configurações',
                'db_table': 'Aprovacao_Config',
                'unique_together': {('configuracao', 'pessoa')},
            },
        ),
    ]
