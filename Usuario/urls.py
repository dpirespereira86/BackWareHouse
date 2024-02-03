from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import PerfilViewSet,obtain_auth_token
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views

router_usuario = SimpleRouter()
router_usuario.register('',PerfilViewSet)


urlpatterns = [
  path('api-token-auth/',obtain_auth_token)
]

