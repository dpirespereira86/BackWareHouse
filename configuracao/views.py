from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from Usuario.models import Usuario
from empresa.models import Empresa
from .models import Configuracao,Aprovacao_Config
from .serializers import ConfigSerializers


# Create your views here.
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Configuracao.objects.all()
    serializer_class = ConfigSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def create(self, request, *args, **kwargs):
        dados = request.data.copy()
        usuario = Usuario.objects.get(email=request.user)
        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        dados.__setitem__('empresa', empresa.id)

        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

