from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from .models import Configuracao,Aprovacao_Config
from .serializers import ConfigSerializers


# Create your views here.
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Configuracao.objects.all()
    serializer_class = ConfigSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

