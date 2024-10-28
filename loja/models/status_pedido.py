from django.db import models


class StatusPedido(models.Model):
    descricao = models.CharField(max_length=20)

    def __str__(self) -> str:
        return "%s" % (self.descricao)
