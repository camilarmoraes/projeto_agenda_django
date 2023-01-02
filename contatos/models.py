from django.db import models
from django.utils import timezone  


# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome #Mudando a representação de classe no admin -> nome da categoria

    
class Contato(models.Model): #Herdando de Model
    # ID como sempre é automático
    #Criar atributos de classe
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255, blank=True) #Campo opcional
    telefone = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    descricao = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)# Relação entre as tabelas

    def __str__(self):
        return self.nome #Aparecerá o nome



