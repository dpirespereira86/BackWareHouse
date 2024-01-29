from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router_pedido = SimpleRouter()
router_pedido.register('aprovacao',views.AprovacaoViewSet)
router_pedido.register('cotacao',views.CotacaoViewSet)
router_pedido.register('item_pedido',views.ItemPedidoCompraViewSet)
router_pedido.register('compra',views.PedidoCompraViewSet)
router_pedido.register('item_solicitacao',views.ItemSolicitacaoViewSet)
router_pedido.register('',views.SolicitacaoViewSet)

urlpatterns = [

]