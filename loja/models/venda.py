from django.db import models
from .cliente import Cliente
from .vendedor import Vendedor


class Venda(models.Model):
    data_pedido = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "%s, %s, %s" % (self.data_pedido, self.cliente.nome, self.vendedor)
