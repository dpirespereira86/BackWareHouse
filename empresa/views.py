import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError,_get_error_details
import requests

from Usuario.models import Usuario
from .models import Empresa,Filial
from .serializers import EmpresaSerializers,FilialSerializers


# Create your views here.
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

    def post_usuario(self,request):
        url = 'http://127.0.0.1:8000/api/v1/usuario'
        id_empresa = Empresa.objects.last()
        data = {
                'first_name': request.data['first_name_responsavel'],
                'last_name': request.data['last_name_responsavel'],
                'email': request.data['email_responsavel'],
                'empresa': str(id_empresa.id + 1)}

        response = requests.post(url, json=data)

        if response.status_code != 201:
            raise _get_error_details(response)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.post_usuario(request)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FilialViewSet(viewsets.ModelViewSet):
    queryset = Filial.objects.all()
    serializer_class = FilialSerializers


    def create(self, request, *args, **kwargs):

        print(request.data)
        #self.salva_empresa(request)
        id_empresa = Empresa.objects.last()
        print('Passei aqui....',id_empresa.id)
        filial = request.data.copy()
        filial.__setitem__('numero_empresa',str(id_empresa.id))
        print(filial)
        serializer = self.get_serializer(data=filial)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EmpresaCreateduserViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        empresa = Empresa.objects.last()
        Usuario.objects.create_superuser(
            email=empresa.email_responsavel,
            password=empresa.senha_inicial,
            first_name=empresa.first_name_responsavel,
            last_name=empresa.last_name_responsavel,
            empresa=empresa,

        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

