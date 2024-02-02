from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

from Produto.models import Produto
from configuracao.models import Aprovacao_Config
from Usuario.models import Usuario
from configuracao.models import Configuracao
from empresa.models import Empresa
from .models import Solicitacao,PedidoCompra,ItemSolicitacao,ItemPedidoCompra,Cotacao,ItemCotacao,AprovacaoSolicitacao
from .serializers import (SolictacaoSerializers,PedidoCompraSerializers,
                          ItemPedidoCompraSerializers,ItemSolicitacaoSerializers,CotacaoSerializers,AprovacaoSerializers)
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
        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        print()
        if not aprovacao_config.filter(pessoa=request.user):
            raise APIException('Usuário não pode aprovar')

        """
         Verifica quantidade de aprovações necessárias e quantas tem 
        """
        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if configuracao.geracao_pedido_auto == True:
            x = 0
            if len(aprovacao_solictacao) == len(aprovacao_config):
                for aprovacao in aprovacao_config:
                    if aprovacao_solictacao.filter(usuario=aprovacao.pessoa):
                        x=x+1

        if x == len(aprovacao_config):
            PedidoCompra.objects.create(
                operador = usuario,
                solicitante= solicitacao.solicitante,
                observacao = '',
                imagem = '',
                empresa = empresa,
                estimativa_valor = 0.00,
                valor_pedido=0.00,
                prazo_de_entrega=0,
                nf='',
            )

            pedido = PedidoCompra.objects.last()
            print(pedido)
            itens = ItemSolicitacao.objects.filter(solicitacao=solicitacao.id)

            for item in itens:

                ItemPedidoCompra.objects.create(
                    pedido_compra=pedido,
                    codigo=item.codigo,
                    descricao=item.descricao,
                    quantidade=item.quantidade,
                    prazo_de_entrega=0,
                    valor_unitario=0.00,
                    valor_total=0,
                    fornecedor=Produto.objects.get(codigo=item.codigo).fornecedor
                )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)