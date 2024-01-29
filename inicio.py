from empresa.models import Empresa
from Usuario.models import Usuario


def cria_inicio():
    if not Empresa.objects.last():
        empresa = Empresa(
            razao_social ='2D projetos',
            cnpj = '0000000000000',
            endereco = 'Rua cel frencisco lima ',
            numero = '120',
            bairro = 'Gradim',
            cidade = 'São gonçalo',
            uf = 'Rj',
            telefone = '21975051275',
            first_name_responsavel = 'Diogo',
            last_name_responsavel = 'Pires',
            email_responsavel = '2dprojetos@2dprojetos.com.br',
            telefone_responsavel = '21975051275',
            wms = 'True',
            compras = 'False',
            frota = 'False',
            ativo = 'True',
            senha_inicial = '8838',
        )
        empresa.save()

        Usuario.objects.create_user(
            email=empresa.email_responsavel,
            username= empresa.email_responsavel,
            password=empresa.senha_inicial,
            is_superuser=True,
            first_name=empresa.first_name_responsavel,
            last_name = empresa.last_name_responsavel,
            empresa=empresa
            )

