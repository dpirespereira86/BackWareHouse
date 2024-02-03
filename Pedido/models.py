from django.db import models

from Usuario.models import Usuario
from empresa.models import Empresa, Fornecedor
from Produto.models import Produto


# Create your models here.
class Base(models.Model):
    criacao = models.DateTimeField('Data Criação',auto_now_add=True)
    modificado = models.DateTimeField('Atualização',auto_now=True)

    class Meta:
        abstract=True
class Solicitacao(Base):

    id = models.AutoField(primary_key=True)
    solicitante = models.ForeignKey(Usuario, related_name=
    'solictacoes_de_compra', on_delete=models.CASCADE)
    observacao = models.TextField(max_length=200, blank=True, null=True)
    urgencia = models.BooleanField(verbose_name='Urgente', default=False)
    justificativa = models.TextField(verbose_name='justificativa', blank=True, null=True)
    empresa = models.ForeignKey(Empresa,related_name='solicitacoes',on_delete=models.CASCADE)
    valor_estimado = models.BooleanField(default=False, blank=True, null=True)
    descricao = models.TextField(verbose_name='observação', blank=False, null=False)

    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        verbose_name = "Solicitacão Compra"
        verbose_name_plural = "Solicitacões Compras"
        unique_together = ["id", "empresa"]
        db_table = "Solicitacao_compra"


class ItemSolicitacao(Base):
    id = models.AutoField(primary_key=True,unique=True)
    solicitacao = models.ForeignKey(Solicitacao,related_name='itens_solicitacoes',on_delete=models.CASCADE,blank=True,
                                    null=True)
    codigo=models.ForeignKey(Produto,related_name='itens_solicitacoes',on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)

    def __str__(self):
        return f'{self.solicitacao}'

    class Meta:
        verbose_name = "Item_Solicitacão"
        verbose_name_plural="Itens_Solicitações"
        db_table = "Item_Solicitacao"

class ItemAvulso(Base):
    id = models.AutoField(primary_key=True, unique=True)
    solicitacao = models.ForeignKey(Solicitacao, related_name="itens_avulso",on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    imagem = models.ImageField(default='', upload_to='imagem_solicitacao', null=True, blank=True)
    fornecedor_indicado = models.CharField(max_length=100,blank=True,null=True)
    total = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        verbose_name = "Item Avulso Solicitação "
        verbose_name_plural = "Itens Avulsos Solictação"
        db_table = "Item_Avulso_Solicitacao"


class AprovacaoSolicitacao(Base):
    usuario = models.ForeignKey(verbose_name='Usuarios',to=Usuario,related_name=
    'aprovacoes',on_delete=models.CASCADE)
    justificativa = models.TextField(verbose_name='Observação',blank=True,null=True)
    aprovado = models.BooleanField('Aprovado',default=False)
    solicitacao = models.ForeignKey(Solicitacao, related_name='aprovacoes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.solicitacao} - {self.justificativa}'

    class Meta:
        verbose_name = "Aprovação de Solicitação"
        verbose_name_plural = "Aprovações de Solicitações"
        db_table = "Aprovacao_Solicitacao_de_Compra"
        unique_together = ["usuario", "solicitacao"]


class PedidoCompra(Base):

    id = models.AutoField(primary_key=True)
    operador = models.ForeignKey(Usuario,related_name='pedido_compras',on_delete=models.CASCADE)
    solicitante = models.CharField(max_length=30, null=False, blank=False)
    observacao = models.TextField(max_length=200, blank=True, null=True)
    imagem = models.ImageField(default='', null=True, blank=True)
    empresa = models.ForeignKey(Empresa,related_name='pedido_compras',on_delete=models.CASCADE)
    estimativa_valor = models.DecimalField(max_digits=5,decimal_places=2)
    valor_pedido = models.DecimalField(max_digits=5,decimal_places=2)
    prazo_de_entrega = models.IntegerField(default=0, null=True, blank=True)
    nf = models.FileField(upload_to='arquivo/nf',blank=True, null=True)



    def __str__(self):
        return f'{self.id}-{self.solicitante}'

    class Meta:
        verbose_name = "Pedido de Compra"
        verbose_name_plural = "Pedidos de Compra"
        unique_together = ["id", "empresa"]
        db_table = "Pedido_compra"


class ItemPedidoCompra(Base):

    id = models.AutoField(primary_key=True,unique=True)
    pedido_compra = models.ForeignKey(PedidoCompra,related_name='itens_pedido_compra',on_delete=models.CASCADE,
                                      blank=True,null=True)
    codigo=models.ForeignKey(Produto,related_name='itens_pedido_compra',on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)
    prazo_de_entrega = models.IntegerField(default=0, null=True, blank=True)
    valor_unitario = models.DecimalField(max_digits=5,decimal_places=2)
    valor_total = models.DecimalField(max_digits=5, decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor, related_name='itens_pedido_compra', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pedido_compra}'

    class Meta:
        verbose_name = "Item Pedido de Compra"
        verbose_name_plural="Itens Pedido de Compra"
        db_table = "Item_Pedido_Compra"

class ItemAvulsoPedido(Base):
    id = models.AutoField(primary_key=True, unique=True)
    pedido_compra = models.ForeignKey(PedidoCompra, related_name="itens_pedido_avulso",on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    fornecedor_indicado = models.CharField(max_length=100,blank=True,null=True)
    total = models.DecimalField(max_digits=5, decimal_places=2,blank=True,null=True)
    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        verbose_name = "Item Avulso Pedido "
        verbose_name_plural = "Itens Avulsos Pedido"
        db_table = "Item_Avulso_Pedido"


class Cotacao(Base):

    id = models.AutoField(primary_key=True)
    operador = models.CharField(max_length=30, null=False, blank=False)
    pedido_compra = models.ForeignKey(PedidoCompra, related_name='cotacoes', on_delete=models.CASCADE)
    fornecedor = models.CharField(max_length=30, null=False, blank=False)
    contato = models.CharField(max_length=30, null=False, blank=False)
    email_contato = models.EmailField()
    observacao = models.TextField(max_length=200, blank=True, null=True)
    empresa = models.ForeignKey(Empresa,related_name='cotações',on_delete=models.CASCADE)
    valor_pedido = models.DecimalField(max_digits=5, decimal_places=2)
    prazo_de_entrega = models.IntegerField(default=0, null=True, blank=True)
    orcamento = models.FileField(upload_to='arquivo/orcamento',blank=True,null=True)
    justificativa= models.TextField(max_length=200, blank=True, null=True)
    fechado = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.pedido_compra}'

    class Meta:
        verbose_name = "Cotacão"
        verbose_name_plural="Cotações"
        db_table = "Cotacao"


class ItemCotacao(Base):
    id = models.AutoField(primary_key=True, unique=True)
    cotacao = models.ForeignKey(Cotacao, related_name="itens_cotacoes",on_delete=models.CASCADE)
    codigo = models.ForeignKey(Produto, related_name='itens_cotacoes', on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    empresa = models.CharField(max_length=30, null=False, blank=False)
    ultimo_preco=models.DecimalField(max_digits=5, decimal_places=2)
    valor_unit = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor, related_name='itens_cotacoes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.codigo}-{self.descricao}'

    class Meta:
        verbose_name = "Item_cotacao"
        verbose_name_plural = "Itens_cotacao"
        db_table = "Item_cotacao"
