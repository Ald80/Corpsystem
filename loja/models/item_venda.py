from django.db import models
from .venda import Venda
from .cliente import Cliente
from .produto import Produto
from .vendedor import Vendedor
from .status_pedido import StatusPedido

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    # cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    # vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    quantidade_vendida = models.IntegerField()
    status_pedido = models.ForeignKey(StatusPedido, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "%s, %s, %s, %s" % (self.venda, self.produto, self.quantidade_vendida, self.status_pedido)