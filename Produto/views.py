import requests
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from .models import Produto,Familia
from .serializers import ProdutoSerializers,FamiliaSerializers,ProdutoEstoqueSerializers
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from Usuario.models import Usuario

# Create your views here.
class ProdutoViewSet(viewsets.ModelViewSet):

    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]


    def preencheempresa(self, request):
        """
         realiza o preencimento automático do código interno e descrição

        """
        usuario = Usuario.objects.get(email=request.user)
        dados = request.data.copy()
        dados.__setitem__('empresa', f'{usuario.empresa}')
        return dados

    def create(self, request, *args, **kwargs):
        """
           Metodo django de sobreescrito
        """
        unidade = self.preencheempresa(request)
        serializer = self.get_serializer(data=unidade)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        usuario = Usuario.objects.get(email=request.user)
        queryset = queryset.filter(empresa=usuario.empresa)
        empresa = requests.get(f'http://127.0.0.1:8080/api/v1/empresa/{usuario.empresa}').json()

        for filial in empresa['filiais']:
            queryset_temp = Produto.objects.filter(empresa=filial)
            queryset = queryset | queryset_temp

        if empresa['ativo'] == True:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise ValidationError('Empresa descredenciada')


class ProdutoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoEstoqueSerializers
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())
        usuario = Usuario.objects.get(email=request.user)
        queryset = queryset.filter(empresa=usuario.empresa)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class FamiliaViewSet(viewsets.ModelViewSet):
    queryset = Familia.objects.all()
    serializer_class = FamiliaSerializers
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        usuario = Usuario.objects.get(email=request.user)
        queryset = queryset.filter(empresa=usuario.empresa)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

