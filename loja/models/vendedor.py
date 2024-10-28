from django.db import models


class Vendedor(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "%s" % (self.nome)
