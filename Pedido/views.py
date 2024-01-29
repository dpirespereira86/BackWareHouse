from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Solicitacao,PedidoCompra,ItemSolicitacao,ItemPedidoCompra,Cotacao
from .serializers import (SolictacaoSerializers,PedidoCompraSerializers,
                          ItemPedidoCompraSerializers,ItemSolicitacaoSerializers,CotacaoSerializers)

# Create your views here.
class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolictacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

class PedidoCompraViewSet(viewsets.ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

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