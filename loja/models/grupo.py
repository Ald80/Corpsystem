from django.db import models

class Grupo(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.descricao