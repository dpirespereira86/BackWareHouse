from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('cria_user',views.EmpresaCreateduserViewSet)
router.register('filial',views.FilialViewSet)
router.register('',views.EmpresaViewSet)

