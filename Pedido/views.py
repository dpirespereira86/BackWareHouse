from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

from Produto.models import Produto
from configuracao.models import Aprovacao_Config
from Usuario.models import Usuario
from configuracao.models import Configuracao
from empresa.models import Empresa
from .models import (Solicitacao,PedidoCompra,ItemSolicitacao,ItemPedidoCompra,Cotacao,ItemCotacao,AprovacaoSolicitacao,
                     ItemAvulsoPedido,ItemAvulso)
from .rules import permissao_aprovar, verifica_ultima_aprovacao, filtra_solicitacao_sem_aprovacao_por_nivel, \
    valor_estimado
from .serializers import (SolictacaoSerializers, PedidoCompraSerializers,
                          ItemPedidoCompraSerializers, ItemSolicitacaoSerializers,
                          CotacaoSerializers,AprovacaoSerializers,
                          SolicitacaoSemAprovacaoSerializers, CotacaoOrcamentoSerializers,
                          FechamentoCotacaoSerializers)
from rest_framework.exceptions import APIException


# Create your views here.
class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolictacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        usuario = Usuario.objects.get(email=request.user)
        dados.__setitem__('solicitante',int(usuario.id))
        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        dados.__setitem__('empresa', empresa.id)
        # Soma os valoes dos itens para fechar o valor da SC
        dados.__setitem__('valor_estimado',
                          valor_estimado(
                              request.data['itens_solicitacoes'],
                              request.data['itens_avulso']))

        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

class PedidoCompraViewSet(viewsets.ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        usuario = Usuario.objects.get(email=request.user)
        dados.__setitem__('operador', usuario.id)

        solicitacao = Solicitacao.objects.get(id=request.data['solicitacao'])
        print(solicitacao.solicitante.id)
        dados.__setitem__('solicitante',solicitacao.solicitante.id)

        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        dados.__setitem__('empresa', empresa.id)

        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ItemSolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = ItemSolicitacao.objects.all()
    serializer_class =  ItemPedidoCompraSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

class ItemPedidoCompraViewSet(viewsets.ModelViewSet):
    queryset = ItemSolicitacao.objects.all()
    serializer_class = ItemSolicitacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

class CotacaoViewSet(viewsets.ModelViewSet):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        #adiciona usuário
        usuario = Usuario.objects.get(email=request.user)
        dados.__setitem__('operador',usuario.id)
        # adiciona empresa
        dados.__setitem__('empresa', Empresa.objects.get(razao_social=usuario.empresa).id)
        valor_cotacao=0
        for item in request.data['itens_cotacoes']:
            valor_cotacao=(float(item['valor_unit']) * float(item['quantidade'])) + valor_cotacao

        dados.__setitem__('valor_cotacao',valor_cotacao )
        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class CotacaoOrcamentoViewSet(viewsets.ModelViewSet):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoOrcamentoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

class FechamentoCotacaoViewSet(viewsets.ModelViewSet):
    queryset = Cotacao.objects.all()
    serializer_class = FechamentoCotacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        empresa = Empresa.objects.get(razao_social=instance.empresa)
        configuracao=Configuracao.objects.get(empresa=empresa.id)
        if len(request.data['fechado']) == 4:
            if str(instance.fechado) == request.data['fechado']:
                raise APIException('Status já realizado')
            contacoes = Cotacao.objects.filter(pedido_compra=instance.pedido_compra)
            if len(contacoes) != configuracao.quantidade_cotacao:
                raise APIException(f'Pedido não tem {configuracao.quantidade_cotacao} cotações')
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            itens = ItemCotacao.objects.filter(cotacao=instance.id)
            # implementar o celery
            valores = 0
            contador = 0
            itens_gerais=[]
            for item in itens:
                produto= Produto.objects.get(codigo=item.codigo)
                produto.ultimo_preco = item.valor_unit
                cotacoes = Cotacao.objects.filter(empresa=empresa.id)
                print(cotacoes)
                for cotacao in cotacoes:
                    if cotacao.fechado:
                        itens_gerais.append(ItemCotacao.objects.filter(cotacao=cotacao.id,codigo=item.codigo))
                print(itens_gerais)
                for item_geral in itens_gerais:
                    print(item_geral.values())
                    valores = float(item_geral[0].valor_unit) + valores
                    contador = contador + 1
                produto.preco_medio = valores / contador
                produto.save()
            # implementar o celery

            #TODO:  recebimento de prazo de de entrega representante almoxarife //
            # TODO: verificar o campo empresa de ItemCotacao //
        else:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ItemCotacaoViewSet(viewsets.ModelViewSet):
    queryset = ItemCotacao.objects.all()
    serializer_class = CotacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

class AprovacaoViewSet(viewsets.ModelViewSet):
    queryset = AprovacaoSolicitacao.objects.all()
    serializer_class = AprovacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        usuario = Usuario.objects.get(email=request.user)
        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        dados.__setitem__('usuario', usuario.id)

        configuracao = Configuracao.objects.get(empresa=empresa.id)
        solicitacao = Solicitacao.objects.get(id=request.data['solicitacao'])
        aprovacao_solictacao = AprovacaoSolicitacao.objects.filter(solicitacao=solicitacao.id)
        aprovacao_config = Aprovacao_Config.objects.filter(configuracao=configuracao.id)
        """
         Saber se o usuario tem permissão para aprovar 
        """
        permissao_aprovar(request.user,aprovacao_config)
        """
         Verifica quantidade de aprovações necessárias e quantas tem 
        """
        verifica_ultima_aprovacao(aprovacao_config,
                                               request.data['aprovado'],solicitacao,
                                               usuario,empresa,configuracao,
                                               aprovacao_solictacao,request.data['justificativa'])
        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

class SolicitacaoSemAprovacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSemAprovacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        usuario = Usuario.objects.get(email=request.user)
        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        configuracao = Configuracao.objects.get(empresa=empresa.id)
        aprovacao_config = Aprovacao_Config.objects.filter(configuracao=configuracao.id)
        queryset = queryset.filter(empresa=empresa)
        newquery = filtra_solicitacao_sem_aprovacao_por_nivel(queryset,
                                                              AprovacaoSolicitacao,
                                                              aprovacao_config,
                                                              request.user)
        page = self.paginate_queryset(newquery)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(newquery, many=True)
        return Response(serializer.data)