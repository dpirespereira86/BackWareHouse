
from . import views
from rest_framework.routers import SimpleRouter

router_notification = SimpleRouter()
router_notification.register('count',views.CountNotificacaoViewSet)
router_notification.register('',views.NotificacaoViewSet)