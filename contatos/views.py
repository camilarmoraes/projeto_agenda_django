from django.shortcuts import render, get_object_or_404, redirect #Atalho para erro 404
from .models import Contato
from django.http import Http404 #Levantamento de erro
from django.core.paginator import Paginator
from django.db.models import Q, Value #Consultas mais complexas
from django.db.models.functions import Concat
from django.contrib import messages
# Create your views here.

def index(request):
    #messages.add_message(request,messages.ERROR,'Ocorreu um erro!')
    contatos = Contato.objects.all() #Pegando com valores
    #contatos = Contato.objects.get_queryset().order_by('id') #problema de queryset
    #contatos = Contato.objects.order_by('nome') -> descrecente ('-nome')
    #contatos = Contato.objects.get_queryset().order_by('id').filter(
    # mostrar = True) #filtrando os objetos
    paginator = Paginator(contatos,5) #Paginação
    page = request.GET.get('página')
    contatos = paginator.get_page(page)
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
        #Ver se um contato pode ser mostrado em uma view
        if not contato.mostrar:
            raise Http404()
        return render(request, 'contatos/ver_contato.html',{
             'contato':contato
        })

def busca(request):
    termo = request.GET.get('termo')

    #Levantar erro de None no termo
    if termo is None or not termo:
        #raise Http404()
        messages.add_message(request,messages.ERROR,'O campo não pode ficar vazio')
        messages.add_message(request,messages.SUCCESS,'Teste de Sucesso')
        return redirect('index')


    campos = Concat('nome',Value(' '),'sobrenome')
    # contatos = Contato.objects.order_by('-id').filter(Q(nome__icontains=termo) | Q(sobrenome__icontains=termo)
    #                                                     ,mostrar=True) #Este ou este
    contatos = Contato.objects.annotate(
        nome_completo=campos
    ).filter(
        Q(nome_completo__icontains = termo) | Q(telefone__icontains=termo) #ou nome e sobrenome ou telefone
    )
    paginator = Paginator(contatos,5)
    page = request.GET.get('p')
    contatos = paginator.get_page(page)
    return render(request,'contatos/busca.html',{
        'contatos':contatos
    })
