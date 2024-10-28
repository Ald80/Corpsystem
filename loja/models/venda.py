from django.db import models
from .cliente import Cliente
from .vendedor import Vendedor
from .status_pedido import StatusPedido

class Venda(models.Model):
    data_pedido = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    # status_pedido = models.CharField(max_length=50)
    # status_pedido = models.ForeignKey(StatusPedido, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "%s, %s, %s" % (self.data_pedido, self.cliente.nome, self.vendedor)