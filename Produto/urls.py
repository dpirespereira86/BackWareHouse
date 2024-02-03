from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework.routers import SimpleRouter

router_produto = SimpleRouter()
router_produto.register('familia',views.FamiliaViewSet)
router_produto.register('estoque',views.ProdutoEstoqueViewSet)
router_produto.register('',views.ProdutoViewSet)

urlpatterns = [

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)