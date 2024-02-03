from django.db import models
from empresa.models import Empresa
from Produto.models import Produto
from Usuario.models import Usuario
from Pedido.models import PedidoCompra


# Create your models here.
class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract =True
class Unidade(Base):
    """
        FIFO - Primeiro a entrar, primeiro a sair;
        FEFO - Primeiro a vencer, primeiro a sair;
        LIFO - Último que Entra é o Primeiro que Sair;

    """
    ESTOQUE_CONTROLE_CHOICE = \
        (
            ("FIFO", "1"),
            ("FEFO", "2"),
            ("LIFO", "3")
        )


    nome= models.CharField(max_length=30,unique=True)
    empresa = models.ForeignKey(Empresa,related_name='unidades',on_delete=models.CASCADE)
    controle_estoque = models.CharField(max_length=50,choices=ESTOQUE_CONTROLE_CHOICE)


    def __str__(self):
        return f'{self.nome}'

    class Meta:
        verbose_name = "Unidade"
        verbose_name_plural = "Unidades"
        unique_together = ['nome','empresa']
        db_table = "Unidade"

class Posicao(Base):

    ALFABETO_CHOICE = (
        ("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"),
        ("E", "E"), ("F", "F"), ("G", "G"), ("H", "H"),
        ("I", "I"), ("J", "J"), ("K", "K"), ("L", "L"),
        ("M", "M"), ("N", "N"), ("O", "O"), ("P", "P"),
        ("Q", "Q"), ("R", "R"), ("S", "S"), ("T", "T"),
        ("U", "U"), ("V", "V"), ("W", "W"),("X", "X"),("Y", "Y"),
        ("Z", "Z")
    )

    NUMERO_CHOICE = (
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"),
        ("5", "5"), ("6", "6"), ("7", "7"), ("8", "8"),
        ("9", "9"), ("10", "10"), ("11", "11"), ("12", "13"),
        ("14", "14"), ("15", "15"), ("16", "16"), ("17", "17"),
        ("18", "18"), ("19", "19"), ("20", "20"), ("21", "22"),
        ("23", "23"), ("24", "24"), ("25", "25"), ("26", "26"), ("27", "27"),
        ("28", "28")
    )


    id = models.AutoField(primary_key=True)
    unidade=models.ForeignKey(Unidade,related_name='posicoes',on_delete=models.CASCADE)
    nome = models.CharField(max_length=30,unique=True)
    rua = models.CharField(max_length=30,choices=ALFABETO_CHOICE,null=False,blank=False)
    predio = models.CharField(max_length=30,choices=ALFABETO_CHOICE,null=False,blank=False)
    nivel = models.CharField(max_length=30,choices=NUMERO_CHOICE,null=False,blank=False)
    sequencia = models.CharField(max_length=30,choices=NUMERO_CHOICE,null=False,blank=False)
    capacidade_peso = models.DecimalField(max_digits=6,decimal_places=2,null=False,blank=False)
    peso=models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    empresa = models.ForeignKey(Empresa,related_name='posicoes',on_delete=models.CASCADE)
    capacidade_volume = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False)
    volume = models.DecimalField(max_digits=5,decimal_places=2)
    alto_valor =models.BooleanField(default=False)
    controlados=models.BooleanField(default=False)
    pesados = models.BooleanField(default=False)
    blocados = models.BooleanField(default=False)
    miudezas = models.BooleanField(default=False)
    refrigerados = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Posição"
        verbose_name_plural="Posições"
        unique_together = ['nome', 'empresa']
        db_table = "Posicao"

class MOVIMENTACAO(Base):
    MOVIMENTACAO_CHOICE = (('1', 'Entrada'), ('2', 'Saida'),('3', 'Conferencia_entrada'),
                           ('4', 'Conferencia_saida'),('5', 'Transferência'))
    TIPO_CONFERENCIA_CHOICE = (('1','palete fechado'), ('2','fechado misto'),
                               ('3','Volume'), ('4','Fração'))

    id = models.AutoField(primary_key=True, unique=True)
    tipo = models.CharField(max_length=30, choices=MOVIMENTACAO_CHOICE, null=False, blank=False)
    tipo_conferencia = models.CharField(max_length=100, choices=TIPO_CONFERENCIA_CHOICE, null=False, blank=False)
    date=models.DateField()
    operador = models.ForeignKey(Usuario,related_name='movimentações',on_delete=models.CASCADE)
    posicao = models.ForeignKey(Posicao,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,related_name='movimentacoes',on_delete=models.CASCADE)
    aprovado=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tipo}'

    class Meta:
        verbose_name = "Movimentaçao"
        verbose_name_plural="Movimentações"
        db_table = "Movimentacao"
        unique_together = ['id', 'empresa']



class Item(Base):
    id = models.AutoField(primary_key=True,unique=True)
    codigo=models.ForeignKey(Produto,related_name='itens',on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)
    movimentacao = models.ForeignKey(MOVIMENTACAO,related_name='itens',on_delete=models.CASCADE,blank=True,null=True)
    empresa = models.ForeignKey(Empresa,related_name='itens',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.codigo}'

    class Meta:
        verbose_name = "Item"
        verbose_name_plural="Itens"
        db_table = "Item"



class Estoque(Base):
    posicao = models.ForeignKey(Posicao,on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto,related_name='estoques',on_delete=models.CASCADE)
    quantidade=models.DecimalField(max_digits=5,decimal_places=2)
    empresa = models.ForeignKey(Empresa,related_name='estoques',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.posicao.nome}'

    class Meta:
        verbose_name = "Estoque"
        verbose_name_plural = "Estoques"
        db_table = "Estoque"



class Doca(Base):

    unidade= models.ForeignKey(Unidade,related_name='docas',on_delete=models.CASCADE)
    nome = models.CharField(max_length=50,null=False,blank=False)
    empresa = models.ForeignKey(Empresa,related_name='docas',on_delete=models.CASCADE)
    recebimento = models.BooleanField(default=False)
    expedicao = models.BooleanField(default=False)
    outras=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        verbose_name = "Doca"
        verbose_name_plural = "Docas"
        db_table = "Doca"



class ItensConferencia(Base):
    id = models.AutoField(primary_key=True,unique=True)
    codigo=models.ForeignKey(Produto,related_name='itens_conferencias',on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5,decimal_places=2)
    empresa = models.ForeignKey(Empresa,related_name='itens_conferencias',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.codigo}'

    class Meta:
        verbose_name = "Item_conferencia"
        verbose_name_plural="Itens_conferencias"
        db_table = "Item_Conferencia"


class Conferencia(Base):

    TIPO_CONFERENCIA_CHOICE = (('1','palete fechado'), ('2','fechado misto'),
                               ('3','Volume'), ('4','Fração'))

    FLUXO_CHOICE = (('1','Entrada'), ('2','Saida'),)

    id = models.AutoField(primary_key=True, unique=True)
    tipo_conferencia = models.CharField(max_length=100, choices=TIPO_CONFERENCIA_CHOICE, null=False, blank=False)
    operador = models.ForeignKey(Usuario,related_name='conferencias',on_delete=models.CASCADE)
    posicao = models.ForeignKey(Posicao,on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa,related_name='conferencias',on_delete=models.CASCADE)
    aprovado=models.BooleanField(default=False)
    pedido = models.ForeignKey(PedidoCompra,related_name='conferencias',on_delete=models.CASCADE)
    nf= models.IntegerField()
    itens_conferencia = models.ForeignKey(ItensConferencia,related_name='conferencias',on_delete=models.CASCADE)
    fluxo = models.CharField(max_length=100, choices=FLUXO_CHOICE, null=False, blank=False)

    def __str__(self):
        return f'{self.tipo_conferencia}'

    class Meta:
        verbose_name = "Conferencia"
        verbose_name_plural="Conferências"
        db_table = "Conferencia"
        unique_together = ['id', 'empresa']

class Transitorio(Base):

    id = models.AutoField(primary_key=True, unique=True)
    codigo = models.ForeignKey(Produto, related_name='itens_transitorios', on_delete=models.CASCADE)
    codigo_interno = models.CharField(max_length=30)
    descricao = models.CharField(max_length=100)
    quantidade = models.DecimalField(max_digits=5, decimal_places=2)
    conferencia = models.ForeignKey(Conferencia, related_name='itens_transitorios', on_delete=models.CASCADE, blank=True,
                                     null=True)
    empresa = models.ForeignKey(Empresa, related_name='itens_transitorios', on_delete=models.CASCADE)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.tipo_conferencia}'

    class Meta:
        verbose_name = "Transitorio"
        verbose_name_plural= "Transitórios"
        db_table = "Transitorio"
        unique_together = ['id', 'empresa']