from django.db import models
from .grupo import Grupo

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "%s, %s, %s" % (self.nome, self.preco, self.grupo)
