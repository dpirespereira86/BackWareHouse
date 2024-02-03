from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter



router_config = SimpleRouter()

router_config.register('',views.ConfigViewSet)