from rest_framework.exceptions import APIException
from Pedido.models import (PedidoCompra, ItemPedidoCompra, ItemSolicitacao,
                           ItemAvulso, ItemAvulsoPedido)
from Produto.models import Produto
from notifications.signals import notify
from django.core.mail import send_mail




def busca_item_solicitacao(solicitacao):
  itens_avulso = ItemAvulso.objects.filter(solicitacao=solicitacao.id)
  return itens_avulso
def busca_item_solicitacao(solicitacao):
  itens = ItemSolicitacao.objects.filter(solicitacao=solicitacao.id)
  return itens

def create_item_pedido_avulso(solicitacao,pedido):
    itens = busca_item_solicitacao(solicitacao)
    for item in itens :
        ItemAvulsoPedido.objects.create(
            pedido_compra=pedido,
            descricao=item.descricao,
            quantidade=item.quantidade,
            fornecedor_indicado='',
            total=0.00,
        )
def create_item_pedido(pedido_compra,solicitacao):
  itens = busca_item_solicitacao(solicitacao)
  for ite in itens:
      ItemPedidoCompra.objects.create(
          pedido_compra=pedido_compra,
          codigo=ite.codigo,
          descricao=ite.descricao,
          quantidade=ite.quantidade,
          prazo_de_entrega=0,
          valor_unitario=0.00,
          valor_total=0,
          fornecedor=Produto.objects.get(codigo=ite.codigo).fornecedor
      )


def convert_solictacaoo_pedido(solicitacao,
                               usuario,empresa):
    PedidoCompra.objects.create(
        operador=usuario,
        solicitante=solicitacao.solicitante,
        observacao='',
        imagem='',
        empresa=empresa,
        estimativa_valor=solicitacao.valor_estimado,
        valor_pedido=0.00,
        prazo_de_entrega=0,
        nf='',
    )
    return PedidoCompra.objects.last()

def permissao_aprovar(user,config_aprovacao):
    if not config_aprovacao.filter(pessoa=user):
        raise APIException('Usuário não possui permissão para aprovar este pedido, '
                           'procure o administrador do sistema')

def count_aprovacao(configuracao,aprovacao_solictacao):
    x=0
    if configuracao.geracao_pedido_auto == True:
            for aprovacao in aprovacao_solictacao:
                if aprovacao.aprovado == True:
                    x = x + 1
    return int(x)

def verifica_ultima_aprovacao(aprovacao_config,aprovado,solicitacao,
                              usuario,empresa,configuracao,aprovacao_solictacao,justificativa):
    if (count_aprovacao(configuracao,aprovacao_solictacao) + 1 == len(aprovacao_config)
            and bool(aprovado) == True):
        pedido = convert_solictacaoo_pedido(solicitacao,usuario,empresa)
        create_item_pedido(pedido,solicitacao)
        create_item_pedido_avulso(solicitacao,pedido)

        notify.send(usuario, recipient=solicitacao.solicitante, verb=f'SC nº:{solicitacao.id} está '
                                                    f'foi aprovada e gerou o PC nº{pedido.id}', )
        send_mail(f'SC nº:{solicitacao.id} Aprovada!', f'SC nº:{solicitacao.id} está '
                                                    f'foi aprovada e gerou o PC nº{pedido.id}'
                  , 'sistema@2dprojetos.com', [solicitacao.solicitante])
    else:
        if aprovado == True:
            nivel = aprovacao_config.get(pessoa=usuario).nivel
            pessoa = aprovacao_config.get(nivel=nivel + 1).pessoa
            notify.send(usuario,recipient= pessoa, verb=f'SC nº:{solicitacao.id} está '
                                              f'aguardando aprovação',)
            send_mail('Solicitção de Aprovacao de Pedido',f'SC nº:{solicitacao.id} está '
                                              f'aguardando aprovação','2dprojetos@2dprojetos.com',
                      [pessoa])
        else:
           notify.send(usuario,recipient=solicitacao.solicitante,
                       verb=f'SC nº{solicitacao.id} não autorizada por {usuario},'
                              f' conforme jsutificativa {justificativa}')
           send_mail(f'SC nº:{solicitacao.id} reprovada!', f'SC nº{solicitacao.id} não autorizada por {usuario},'
                              f' conforme jsutificativa {justificativa}'
                     , 'sistema@2dprojetos.com', [solicitacao.solicitante])

def filtra_solicitacao_sem_aprovacao_por_nivel(queryset,AprovacaoSolicitacao,aprovacao_config,
                                               usuario):
    """
    Filtra solictações por usuário pendentes de acordo com o nivel de aprovação configurado
    :param queryset:
    :param AprovacaoSolicitacao:
    :param aprovacao_config:
    :param usuario:
    :return: a solictação pendente para o usua´rio da requisição
    """
    newquery = []
    for query in queryset:
        aprovacao_solicitacao = AprovacaoSolicitacao.objects.filter(solicitacao=query.id)
        count_aprovado = 0
        for aprovacao in aprovacao_solicitacao:
            if aprovacao.aprovado == True:
                count_aprovado = count_aprovado + 1
        if count_aprovado + 1 <= len(aprovacao_config):
            if usuario == aprovacao_config.get(nivel=count_aprovado + 1).pessoa:
                newquery.append(query)
    return newquery

def valor_estimado(itens_solicitacoes,itens_avulso):
    valor_total = 0.00
    for item in itens_solicitacoes:
        produto = Produto.objects.get(id=item['codigo'])
        valor_total = (float(produto.ultimo_preco) * float(item['quantidade'])) + valor_total

    for item_avulso in itens_avulso:
        valor_total = ((float(item_avulso['total']) * float(item_avulso['quantidade']))
                       + valor_total)

    return valor_total