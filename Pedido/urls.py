from django.urls import path
from .views import (AprovacaoViewSet,CotacaoViewSet,ItemPedidoCompraViewSet,PedidoCompraViewSet,ItemSolicitacaoViewSet,
SolicitacaoViewSet)
from rest_framework.routers import SimpleRouter


router_pedido = SimpleRouter()
router_pedido.register('aprovacao',AprovacaoViewSet)
router_pedido.register('cotacao',CotacaoViewSet)
router_pedido.register('item_pedido',ItemPedidoCompraViewSet)
router_pedido.register('compra',PedidoCompraViewSet)
router_pedido.register('item_solicitacao',ItemSolicitacaoViewSet)
router_pedido.register('',SolicitacaoViewSet)

urlpatterns = [

]