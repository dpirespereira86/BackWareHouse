from rest_framework.exceptions import ValidationError
from Armazem.models import Item, Estoque, MOVIMENTACAO
from Produto.models import Produto, Embalagem
from Usuario.models import Usuario


def restricao_volume(posicao, volume, quantidade):
    volume_total = volume * quantidade
    if (volume_total + float(posicao.volume)) > float(posicao.capacidade_volume):
        raise ValidationError(f'Movimentacao não permitida peso excedido para posição {posicao.nome}')
    else:
        """
        Salvar volume na posição....

        """
        posicao.volume = float(posicao.volume) + float(volume)
        posicao.save()

def restricao_capacidade(posicao, peso, quantidade):
    peso_total = peso * quantidade
    if (peso_total + float(posicao.peso)) > float(posicao.capacidade):
        raise ValidationError(f'Movimentacao não permitida peso excedido para posição {posicao.nome}')
    else:
        """
        Salvar Peso na posição....

        """
        posicao.peso = float(posicao.peso) + float(peso_total)
        posicao.save()


def preenche_campos_movimenta_item(request):
        """
         realiza o preencimento automático do código interno e descrição
        """
        dado = request.data.copy()
        itens= request.data['itens']
        usuario = Usuario.objects.get(email=request.user)
        g = []
        for item in itens:

            if not Produto.objects.filter(codigo=item['codigo'],empresa = usuario.empresa):

                embalagem = Embalagem.objects.get(codigo=item['codigo'], empresa=usuario.empresa)

                nume = Item.objects.last()
                if nume == None:
                    item['codigo'] = f'{embalagem.produto.id}'
                    item['codigo_interno'] = f'{embalagem.produto.codigo}-{1}'
                    item['descricao'] = embalagem.produto.descricao
                    item['empresa'] = usuario.empresa
                    item['quantidade'] = float(embalagem.quantidade_produto) * float(item['quantidade'])
                else:
                    item['codigo'] = f'{embalagem.produto.id}'
                    item['codigo_interno'] = f'{embalagem.produto.codigo}-{nume.id + 1}'
                    item['descricao'] = embalagem.produto.descricao
                    item['quantidade'] = float(embalagem.quantidade_produto) * float(item['quantidade'])
                    item['empresa'] = usuario.empresa
            else:
                produto = Produto.objects.get(codigo=item['codigo'], empresa=usuario.empresa)
                nume = Item.objects.last()

                if nume == None:

                    item['codigo'] = f'{produto.id}'
                    item['codigo_interno'] = f'{produto.codigo}-{1}'
                    item['descricao'] = produto.descricao
                    item['empresa'] = usuario.empresa

                else:
                    item['codigo'] = f'{produto.id}'
                    item['codigo_interno'] = f'{produto.codigo}-{nume.id + 1}'
                    item['descricao']= produto.descricao
                    item['empresa'] =  usuario.empresa

            g.append(item)

        dado.__setitem__('itens', g)
        return dado

def preenche_usuario(request):
    """
     realiza o preencimento automático do código interno e descrição

    """
    produto = Produto.objects.get(id=int(request.data['codigo']))
    dados = request.data.copy()
    nume = Item.objects.last()
    if nume == None:
        dados.__setitem__('codigo_interno', f'{produto.codigo}-{1}')
    else:
        dados.__setitem__('codigo_interno', f'{produto.codigo}-{nume.id + 1}')
    dados.__setitem__('descricao', produto.descricao)
    return dados


def ponto_de_pedido(produto, minimo, estoque_seguranca, opcao, saldo):
        """
          Verifica se a movimentação excedeu o Ponto de Pedido
        """
        s = minimo + ((minimo * estoque_seguranca) / 100)
        if saldo <= s:
            raise ValidationError(f'Ponto de compra atingido para {produto.codigo} - {produto.descricao}')


def estoque_minimo(produto, minimo, saldo):
        """
            Verifica se a moviemntação excedeu o Pondo de Pedido
        """
        if saldo <= minimo:
            raise ValidationError(f'Estoque Minimo atingido para {produto.codigo} - {produto.descricao}')

def estoque_maximo(produto, saldo, maxi):
        if saldo >= maxi:
            raise ValidationError(f'Estoque Máximo atingido {saldo}/{maxi} para {produto.codigo} - {produto.descricao}')

def SalvaSaldoProduto(Produto, tipo_movimentacao, valor):
        """
          Verifica se a movimentação excedeu o Ponto de Pedido
        """
        if tipo_movimentacao == '1':
            Produto.saldo = float(Produto.saldo) + float(valor)
            Produto.save()
        if tipo_movimentacao == '2':
            Produto.saldo = float(Produto.saldo) - float(valor)
            Produto.save()
            ponto_de_pedido(Produto, Produto.estoque_minimo, Produto.estoque_seguranca, Produto.auto_solicitacao,
                                 Produto.saldo)
            estoque_minimo(Produto, Produto.estoque_minimo, Produto.saldo)

def entrada(request, movimentacao, produto, estoque,empresa):
        """
            Realiza a movimentacao de Entrada
        """
        if not estoque:
            try:
                Estoque.objects.create(posicao=movimentacao.posicao, produto=produto,
                                       quantidade=float(request.data['quantidade']),empresa=empresa)
                restricao_capacidade(movimentacao.posicao, float(produto.peso), float(request.data['quantidade']))
                restricao_volume(movimentacao.posicao, float(produto.volume), float(request.data['quantidade']))
                SalvaSaldoProduto(produto, movimentacao.tipo, request.data['quantidade'])
            except:
                raise ValidationError('Não foi possivel salvar Estoque')
        else:
            """
              Verificar Capacidade da Posicao
            """

            restricao_capacidade(movimentacao.posicao, float(produto.peso), float(request.data['quantidade']))

            """
               Soma e salva valor no estoque....
            """

            saldo = float(estoque[0].quantidade) + float(request.data['quantidade'])
            e = Estoque.objects.get(id=int(estoque[0].id))
            e.quantidade = saldo
            e.save()

            """
            Salvar Saldo Produto
            """

            SalvaSaldoProduto(produto, movimentacao.tipo, request.data['quantidade'])
            """
            Alerta de Estoque máximo
            """
            estoque_maximo(produto, produto.saldo, produto.estoque_maximo)

def saida(request, estoque, produto, movimentacao,empresa):
        """
            Realiza a movimentacao de Saida
        """
        if float(request.data['quantidade']) > float(estoque[0].quantidade):
            raise ValidationError('Saldo insuficiente')
        else:
            """
                diminue e salva valor do estoque....
            """
            saldo = float(estoque[0].quantidade) - float(request.data['quantidade'])
            e = Estoque.objects.get(id=int(estoque[0].id))
            e.quantidade = saldo
            e.save()
            """
              Salvar Peso na posição....
            """
            movimentacao.posicao.peso = float(movimentacao.posicao.peso) - (
                        float(produto.peso) * float(request.data['quantidade']))
            movimentacao.posicao.volume = float(movimentacao.posicao.volume) - (
                    float(produto.volume) * float(request.data['quantidade']))
            movimentacao.posicao.save()
            SalvaSaldoProduto(produto, movimentacao.tipo, request.data['quantidade'])

def salvaestoque(request):
        """
            Realiza a operaçção de estoque
        """
        print(request.data)
        movimentacao = MOVIMENTACAO.objects.get(id=int(request.data['id']))
        #estoque = Estoque.objects.filter(posicao=movimentacao.posicao, produto=produto)
        usuario = Usuario.objects.get(email=request.user)

        for item in request.data['itens']:
            if movimentacao.tipo == '1':  # Entrada
                if request.data['tipo_conferencia'] == '1': #palete fechado
                    embalagem = Embalagem.objects.get(codigo=item.codigo)
                    print('embalagem')

                elif request.data['tipo_conferencia'] == '2':#fechado Misto
                    pass
                elif request.data['tipo_conferencia'] == '3': #volume
                    pass
                elif request.data['tipo_conferencia'] == '4': #fração
                    entrada(request, movimentacao, produto, estoque,usuario.empresa)

            if movimentacao.tipo == '2':  # Saida
                pass
                #saida(request, estoque, produto, movimentacao,usuario.empresa)

            if movimentacao.tipo == '1':  # Entrada
                pass
                #entrada(request, movimentacao, produto, estoque,usuario.empresa)


def salvatransitori(request):
    """
        Realiza a operaçção de estoque
    """
    print(request.data)
    movimentacao = MOVIMENTACAO.objects.get(id=int(request.data['id']))
    # estoque = Estoque.objects.filter(posicao=movimentacao.posicao, produto=produto)
    usuario = Usuario.objects.get(email=request.user)

    for item in request.data['itens']:
        if movimentacao.tipo == '1':  # Entrada
            if request.data['tipo_conferencia'] == '1':  # palete fechado
                embalagem = Embalagem.objects.get(codigo=item.codigo)
                print('embalagem')

            elif request.data['tipo_conferencia'] == '2':  # fechado Misto
                pass
            elif request.data['tipo_conferencia'] == '3':  # volume
                pass
            elif request.data['tipo_conferencia'] == '4':  # fração
                entrada(request, movimentacao, produto, estoque, usuario.empresa)

        if movimentacao.tipo == '2':  # Saida
            pass
            # saida(request, estoque, produto, movimentacao,usuario.empresa)

        if movimentacao.tipo == '1':  # Entrada
            pass
            # entrada(request, movimentacao, produto, estoque,usuario.empresa)