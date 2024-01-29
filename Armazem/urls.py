from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('transitorio',views.TransitorioViewSet)
router.register('conferencia',views.ConferenciaViewSet)
router.register('posicao',views.PosicaoViewSet)
router.register('movimentacao/itens',views.MovimentacaoItensViewSet)
router.register('movimentacao/aprovacao',views.AprovacaoMovimentacaoViewSet)
router.register('movimentacao',views.MovimentacaoViewSet)
router.register('item',views.ItemViewSet)
router.register('unidade',views.UnidadeViewSet)
router.register('estoque',views.EstoqueViewSet)

urlpatterns = [

]