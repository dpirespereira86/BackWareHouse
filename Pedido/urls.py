from django.urls import path
from .views import (AprovacaoViewSet, CotacaoViewSet, ItemPedidoCompraViewSet, PedidoCompraViewSet,
                    ItemSolicitacaoViewSet,
                    SolicitacaoViewSet, SolicitacaoSemAprovacaoViewSet, CotacaoOrcamentoViewSet,
                    FechamentoCotacaoViewSet)
from rest_framework.routers import SimpleRouter


router_pedido = SimpleRouter()
router_pedido.register('fechamento',FechamentoCotacaoViewSet)
router_pedido.register('orcamento',CotacaoOrcamentoViewSet)
router_pedido.register('sem_aprovacao',SolicitacaoSemAprovacaoViewSet)
router_pedido.register('aprovacao',AprovacaoViewSet)
router_pedido.register('cotacao',CotacaoViewSet)
router_pedido.register('item_pedido',ItemPedidoCompraViewSet)
router_pedido.register('compra',PedidoCompraViewSet)
router_pedido.register('item_solicitacao',ItemSolicitacaoViewSet)
router_pedido.register('',SolicitacaoViewSet)

urlpatterns = [

]