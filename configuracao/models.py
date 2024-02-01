from django.db import models
from Usuario.models import Usuario
from empresa.models import Empresa


# Create your models here.
class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract =True
class Aprovacao_Config(models.models):
    pessoa=models.ForeignKey(Usuario,related_name='aprovacoes_config',on_delete=models.CASCADE)
    nivel=models.IntegerField()


    def __str__(self):
        return f'{self.pessoa}'
    class Meta:
        verbose_name = "Aprovacao de Configuração"
        verbose_name_plural = "Aprovacões de Configurações"
        db_table = "Aprovacao_Config"
        unique_together = ['pessoa', 'empresa']

class Configuracao(Base):

    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa,related_name='configuracoes',on_delete=models.CASCADE)
    pessoa = models.ForeignKey(Aprovacao_Config,related_name='configuracoes',on_delete=models.CASCADE)
    geracao_pedido_auto = models.BooleanField()

    def __str__(self):
        return f'{self.id}'

    class Meta:
        verbose_name = "Configuração"
        verbose_name_plural = "Configurações"
        db_table = "Configuracao"
        unique_together = ['id', 'empresa']
