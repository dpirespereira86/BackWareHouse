from django.db import models


# Create your models here.
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=30,null=False,blank=False,unique=True)
    cnpj = models.CharField(max_length=30,null=True,blank=True,unique=True)
    endereco = models.CharField(max_length=100,null=False,blank=False)
    numero = models.IntegerField(default=0000-0000)
    bairro =models.CharField(max_length=50,null=False,blank=False,)
    cidade = models.CharField(max_length=50,null=False,blank=False,)
    uf=models.CharField(max_length=2,null=False,blank=False,)
    telefone = models.CharField(max_length=10,null=False,blank=False,)
    first_name_responsavel = models.CharField(max_length=50,null=False,blank=False,)
    last_name_responsavel = models.CharField(max_length=50, null=False, blank=False, )
    email_responsavel = models.EmailField()
    telefone_responsavel = models.CharField(max_length=10,null=False,blank=False,)
    wms= models.BooleanField(default=False)
    compras=models.BooleanField(default=False)
    frota = models.BooleanField(default=False)
    ativo = models.BooleanField(default=False)
    senha_inicial=models.CharField(max_length=8,null=False,blank=False,)
    data_cadastro = models.DateTimeField()

    def __str__(self):
        return f'{self.razao_social}'

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Filial(Empresa):

    matriz = models.ForeignKey(Empresa,related_name='filiais',on_delete=models.CASCADE)
    numero_empresa = models.CharField(max_length=30,null=True,blank=True,default='')


    def __str__(self):
        return f'{self.razao_social}'

    class Meta:
        verbose_name = "Filial"
        verbose_name_plural = "Filiais"





class Fornecedor(models.Model):

    id = models.AutoField(primary_key=True)
    razao_social = models.CharField(max_length=30, null=False, blank=False, unique=True)
    cnpj = models.CharField(max_length=30, null=True, blank=True, unique=True)
    endereco = models.CharField(max_length=100, null=False, blank=False)
    numero = models.IntegerField(default=0000 - 0000)
    bairro = models.CharField(max_length=50, null=False, blank=False, )
    cidade = models.CharField(max_length=50, null=False, blank=False, )
    uf = models.CharField(max_length=2, null=False, blank=False, )
    telefone = models.CharField(max_length=10, null=False, blank=False, )
    contato = models.CharField(max_length=150, null=False, blank=False, )
    email_responsavel = models.EmailField()
    telefone_responsavel = models.CharField(max_length=10, null=False, blank=False, )
    empresa = models.CharField(max_length=10, null=False, blank=False, )
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)
    empresa = models.ForeignKey(Empresa,related_name='fornecedores',on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.razao_social}'

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        db_table = "Fornecedores"