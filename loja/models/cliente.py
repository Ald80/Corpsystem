from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    telefone = models.CharField(max_length=30)

    def __str__(self) -> str:
        return "%s, %s, %s, %s" % (self.nome, self.endereco, self.email, self.telefone)
    

