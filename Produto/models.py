from django.db import models
from django.db.models import UniqueConstraint
from empresa.models import Empresa, Fornecedor


# Create your models here.
class Familia(models.Model):
    nome= models.CharField(max_length=30)
    empresa = models.ForeignKey(Empresa,related_name='familia',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}'

    class Meta:
        verbose_name = "Familia"
        db_table = "Familia"
        unique_together = ["nome", "empresa"]
        db_table = "Familia"


class Produto(models.Model):
    UNIDADE_CHOICE =(
        ("Cj","Conjunto"),("Cx", "Caixa"),("Dz", "Dúzia"),("Fd", "Fardo"),
        ("Fl", "Folha"),("Gl", "Galão"), ("Lt", "Lote"),("Jg", "Jogo"),
        ("Kg", "Kilograma"),("L", "Litro"),("Lta", "Lata"),("M", "Metro"),
        ("Mil", "Milheiro"),("Par", "Par"),("Pct", "Pacote"),("Pç", "Peça"),
        ("Res", "Resma"),("Rl", "Rolo"),("Ton", "Tonelada"),("Und","Unidade"),
        ("Vd", "Vidro"),("M³","Metro_cubico"),("M²","Metro_quadrado"),
    )

    TIPO_CHOICE = (
        ("1", "Matéria-prima"), ("2", "Bens para varejo"), ("3", "Consumo interno da organização"),
        ("4", "Estoque de segurança")

    )

    id= models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=30,null=False,blank=False)
    codigo_Auxiliar = models.CharField(max_length=30,null=True,blank=True,)
    descricao = models.CharField(max_length=100,null=False,blank=False)
    familia= models.ForeignKey(Familia,related_name='produtos',on_delete=models.CASCADE)
    unidade = models.CharField(max_length=30,choices=UNIDADE_CHOICE,null=False,blank=False)
    tipo_item = models.CharField(max_length=60,choices=TIPO_CHOICE,null=False,blank=False)
    ativo = models.BooleanField(default=True)
    especificacao = models.TextField(max_length=200,blank=True,null= True)
    empresa = models.ForeignKey(Empresa,related_name='produtos',on_delete=models.CASCADE)
    observacao = models.TextField(max_length=200,blank=True,null=True)
    imagem= models.ImageField(default='',null=True,blank=True)
    tempo_validade = models.IntegerField(default=0)
    comprimento = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    largura= models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    altura = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    prazo_frete_medio= models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    peso = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    saldo = models.DecimalField(max_digits=6, decimal_places=2,default=0.00)
    estoque_minimo = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    estoque_maximo = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    estoque_seguranca = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    auto_solicitacao=models.BooleanField(default=False)
    fornecedor = models.ForeignKey(Fornecedor,related_name='produtos',on_delete=models.CASCADE)
    volume = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    negativo=models.BooleanField(default=True)
    alto_valor = models.BooleanField(default=False)
    pesados = models.BooleanField(default=False)
    blocados = models.BooleanField(default=False)
    miudezas = models.BooleanField(default=False)
    refrigerados = models.BooleanField(default=False)
    controlados = models.BooleanField(default=False)
    ultimo_preco = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    preco_medio = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)



    def __str__(self):
        return f'{self.codigo}'

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        unique_together = ["codigo","empresa"]
        db_table = "Produto"



class Embalagem(models.Model):
    produto = models.ForeignKey(Produto,related_name='embalagens',on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100,null=False,blank=False)
    codigo =  models.CharField(max_length=30,null=False,blank=False)
    comprimento = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    largura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    altura = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    quantidade_produto = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    volume = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    tipo = models.CharField(max_length=100,null=False,blank=False)
    empresa = models.ForeignKey(Empresa, related_name='embalagens', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.descricao}'

    class Meta:
        verbose_name = "Embalagem"
        verbose_name_plural = "Embalagens"
        db_table = "Embalagem"