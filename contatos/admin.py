from django.contrib import admin
from .models import Categoria, Contato #.models é do próprio app de contatos

# Register your models here.


class ContatoAdmin(admin.ModelAdmin): #Mostrar outros campos
    list_display = ('id','nome','categoria')
    list_display_links = ('id','nome') #Tornar clicável para alteração
    list_filter = ('nome','sobrenome')
    list_per_page = 10 # Exibir 10 elementos por página
    search_fields = ('nome','sobrenome') #Campo de pesquisa

admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)