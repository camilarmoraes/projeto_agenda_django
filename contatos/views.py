from django.shortcuts import render, get_object_or_404 #Atalho para erro 404
from .models import Contato
from django.http import Http404 #Levantamento de erro

# Create your views here.

def index(request):
    contatos = Contato.objects.all() #Pegando com valores
    return render(request, 'contatos/index.html',{
        'contatos':contatos
    })

# def ver_contato(request,contato_id): #visualizar 1
#     try:
#         contato = Contato.objects.get(id=contato_id) #Pegando com valores
#         return render(request, 'contatos/ver_contato.html',{
#             'contato':contato
#         })
#     except Contato.DoesNotExist as e:
#         raise Http404 #Página não existe

def ver_contato(request,contato_id): #visualizar 1
        contato = get_object_or_404(Contato,id=contato_id)
        return render(request, 'contatos/ver_contato.html',{
             'contato':contato
        })


