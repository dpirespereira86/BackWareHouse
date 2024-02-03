"""
URL configuration for company project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Armazem.urls import router
from Produto.urls import router_produto
from Usuario.urls import router_usuario
from Pedido.urls import router_pedido
from empresa.urls import router_empresa
from configuracao.urls import router_config
from notification.urls import router_notification


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('api/v1/produto/', include((router_produto.urls,'Produto'),namespace='Produto')),
    path('api/v1/armazem/', include((router.urls,'Armazem'),namespace='Armazem')),
    path('api/v1/usuario/', include((router_usuario.urls,'Usuario'),namespace='Usuario')),
    path('api/v1/pedido/', include((router_pedido.urls,'Pedido'),namespace='Pedido')),
    path('api/v1/empresa/', include((router_empresa.urls,'empresa'),namespace='empresa')),
    path('api/v1/configuracao/', include((router_config.urls,'configuracao'),namespace='configuracao')),
    path('api/v1/notification/', include((router_notification.urls,'Notification'),namespace='notification')),
    path('api/v1/token/', include('Usuario.urls'))
]

