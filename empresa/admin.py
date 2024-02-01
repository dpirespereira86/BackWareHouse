from django.contrib import admin

# Register your models here.
from empresa.models import Empresa, Filial, Fornecedor


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('id','razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial')

    """
    fieldsets = (
        ('Dados da Empresa', {'fields': ('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone')}),
        ('Dados do Responsável', {'fields': ('first_name_responsavel','last_name_responsavel','email_responsavel',
                                             'telefone_responsavel','senha_inicial')}),
        ('Plano', {'fields': ('wms','compras','frota','ativo')}),
        ('Datas Importantes', {'fields': ('data_cadastro')}),
    )
    """

@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('razao_social','cnpj','numero_empresa','endereco','numero','bairro','cidade','uf','telefone',
    'first_name_responsavel','last_name_responsavel','email_responsavel','telefone_responsavel','wms',
    'compras','frota','ativo','senha_inicial')

    """fieldsets = (
        ('Dados da Filial', {'fields': ('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone')}),
        ('Dados do Responsável', {'fields': ('first_name_responsavel','last_name_responsavel','email_responsavel',
                                             'telefone_responsavel','senha_inicial')}),
        ('Matriz',{'fields':('matriz')}),
        ('Dados da Empresa', {'fields': ('empresa')}),
        ('Plano', {'fields': ('wms','compras','frota','ativo')}),
        ('Datas Importantes', {'fields': ('data_cadastro')}),
    )"""

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('id',
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
    'criacao',
    'atualizacao',
    'empresa',)

    """fieldsets = (
        ('Dados da Filial', {'fields': ('razao_social','cnpj','endereco','numero','bairro','cidade','uf','telefone')}),
        ('Dados do Responsável', {'fields': ('first_name_responsavel','last_name_responsavel','email_responsavel',
                                             'telefone_responsavel','senha_inicial')}),
        ('Matriz',{'fields':('matriz')}),
        ('Dados da Empresa', {'fields': ('empresa')}),
        ('Plano', {'fields': ('wms','compras','frota','ativo')}),
        ('Datas Importantes', {'fields': ('data_cadastro')}),
    )"""

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
    'criacao',
    'atualizacao',
    'empresa',
