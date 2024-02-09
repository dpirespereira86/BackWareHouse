from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response

from Pedido.models import ItemPedidoCompra,ItemAvulsoPedido
from empresa.models import Empresa
from .models import Unidade, Posicao, MOVIMENTACAO, Item, Estoque, Conferencia, Transitorio
from .serializers import (
    UnidadeSerializers,
    PosicaoSerializers,
    MovimentacaoSerializers,
    ItemSerializers,
    EstoqueSerializers,
    MovimentacaoItemSerializers,
    AprovacaoMovimentacaoItemSerializers, ConferenciaSerializers, TransitorioSerializers)

from rest_framework import status
from .rules import *
from Usuario.models import Usuario

# Create your views here.
"""
##################################################### Uunidade #####################################################
"""


class UnidadeViewSet(viewsets.ModelViewSet):
    queryset = Unidade.objects.all()
    serializer_class = UnidadeSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

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


"""
##################################################### Movimentacão #####################################################
"""


class MovimentacaoViewSet(viewsets.ModelViewSet):
    """
    http://127.0.0.1:8000/api/v1/armazem/movimentacao/
    """
    queryset = MOVIMENTACAO.objects.all()
    serializer_class = MovimentacaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

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

    def create(self, request, *args, **kwargs):
        """
           Metodo django de sobreescrito
        """
        movimentacao = request.data.copy()
        usuario = Usuario.objects.get(email=request.user)

        movimentacao.__setitem__('operador', usuario.id)
        movimentacao.__setitem__('empresa', usuario.empresa)

        serializer = self.get_serializer(data=movimentacao)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


"""
##################################################### Movimentacão #####################################################
"""

"""
############################################### Aprovação Movimentacão ################################################
"""


class AprovacaoMovimentacaoViewSet(viewsets.ModelViewSet):
    """
    http://127.0.0.1:8000/api/v1/armazem/movimentacao/
    """
    queryset = MOVIMENTACAO.objects.all()
    serializer_class = AprovacaoMovimentacaoItemSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if request.data:
            if request.data['aprovado'] == 'true':
                print('Entrei')

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)



"""
##################################################### Movimentacão #####################################################
"""
class MovimentacaoItensViewSet(viewsets.ModelViewSet):
    """
    http://127.0.0.1:8000/api/v1/armazem/movimentacao/itens

    """

    queryset = MOVIMENTACAO.objects.all()
    serializer_class = MovimentacaoItemSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]


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


    def create(self, request, *args, **kwargs):
        """
           Metodo django de sobreescrito

        """
        if request.data['tipo'] == '3': #Conferencia_Entrada
            dados = preenche_campos_movimenta_item(request)
            print(dados)
        #dados = preenche_campos_movimenta_item(request)
        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        #self.perform_create(serializer)
        #salvaestoque(request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


"""
##################################################### Itens #####################################################
"""


class ItemViewSet(viewsets.ModelViewSet):
    """
        Movimentacão dos itens, onde são implementas as regras de negócio ...
        http://127.0.0.1:8000/api/v1/armazem/item/
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

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


    def create(self, request, *args, **kwargs):
        """
           Metodo django de sobreescrito para criar objeto
        """
        item = preenche_campos_movimenta_item(request)
        serializer = self.get_serializer(data=item)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        salvaestoque(request)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

"""
##################################################### Estoque #####################################################
"""
class EstoqueViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Estoque.objects.all()
    serializer_class = EstoqueSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

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

"""
##################################################### Posicao #####################################################
"""


class PosicaoViewSet(viewsets.ModelViewSet):
    queryset = Posicao.objects.all()
    serializer_class = PosicaoSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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

    def create(self, request, *args, **kwargs):
        # substituir nome
        posicao = request.data.copy()
        unidade = Unidade.objects.get(id=int(posicao['unidade']))
        usuario = Usuario.objects.get(email=request.user)

        """
        Preenche campos automático
        """

        posicao.__setitem__('nome', f'{unidade} - {request.data["rua"]}{request.data["predio"]}' \
                                    f'{request.data["nivel"]}{request.data["sequencia"]}')
        posicao.__setitem__('empresa',usuario.empresa)

        serializer = self.get_serializer(data=posicao)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ConferenciaViewSet(viewsets.ModelViewSet):
    queryset = Conferencia.objects.all()
    serializer_class = ConferenciaSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def create(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(email=request.user)
        empresa = Empresa.objects.get(razao_social=usuario.empresa)
        dados =  request.data.copy()
        dados.__setitem__('empresa',empresa.id)
        produtos_conferidos = []

        #desmembra os itens conferidos
        for item in request.data['itens_conferencia']:
              if Produto.objects.filter(codigo=item['codigo'],empresa=empresa.id) :
                  print('eu')
                  produto=Produto.objects.get(codigo=item['codigo'],empresa=empresa.id)
                  produtos_conferidos.append(produto)
                  quantidade = item['quantidade']
                  codigo = produto.codigo
                  dados['itens_conferencia'].__setitem__('codigo',produto.id)

              elif Embalagem.objects.filter(codigo=item['codigo']):
                  embalagem = Embalagem.objects.get(codigo=item['codigo'])

                  for i in range(int(embalagem.quantidade_produto)):
                     produto = Produto.objects.get(codigo=embalagem.produto.codigo,empresa=empresa.id)
                     produtos_conferidos.append(produto)
                     codigo = embalagem.produto.codigo
                     quantidade = embalagem.quantidade_produto * item['quantidade']
                     dados['itens_conferencia'].__setitem__('codigo', produto.id)
              else:
                  print('aqui')
                  return Response(f'Produto não encontrado'
                           , status=status.HTTP_428_PRECONDITION_REQUIRED, )
        print(dados)
        # Obtem as quantidades solictadas para cada código no pedido
        if ItemPedidoCompra.objects.filter(id=int(request.data['pedido']), codigo=produto.id):
            itens_pedido = ItemPedidoCompra.objects.filter(id=int(request.data['pedido']), codigo=produto.id)
            itens_pedido_avulso = ItemAvulsoPedido.objects.filter(id=int(request.data['pedido']))
        else:
            return Response(f'Produto {codigo} não existe neste pedido'
                            , status=status.HTTP_428_PRECONDITION_REQUIRED, )

        # Obtem as quantidades solictadas para cada código no pedido
        quantidade_pedido=0
        for item in itens_pedido:
            quantidade_pedido = quantidade_pedido + item.quantidade

        # Conferem se as quantidades conferidas são iguais pedido x conferido
        if quantidade_pedido != quantidade:
            serializer = self.get_serializer(data=dados)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(f'Existe divergencia entre a quantidade de Pedido {quantidade_pedido} e a '
                            f'entrada {quantidade}',status=status.HTTP_428_PRECONDITION_REQUIRED,)


        serializer = self.get_serializer(data=dados)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TransitorioViewSet(viewsets.ModelViewSet):
    queryset = Transitorio.objects.all()
    serializer_class = TransitorioSerializers
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication,SessionAuthentication]