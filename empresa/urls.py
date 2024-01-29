from . import views
from rest_framework.routers import SimpleRouter

router_empresa = SimpleRouter()
router_empresa.register('fornecedor',views.FornecedoresViewSet)
router_empresa.register('cria_user',views.EmpresaCreateduserViewSet)
router_empresa.register('filial',views.FilialViewSet)
router_empresa.register('',views.EmpresaViewSet)

