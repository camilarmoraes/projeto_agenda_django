from django.shortcuts import render, redirect
from django.contrib import messages, auth #auth -> autenticar
from django.core.validators import validate_email #validar email
from django.contrib.auth.models import User #para não repetir determinados dados
from django.contrib.auth.decorators import login_required
from .models import FormContato

# Create your views here.
def index(request):
    return render(request,'accounts/index_login.html')

def login(request):
    if request.method != 'POST':
        return render(request,'accounts/login.html')
    
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user: #se não houver o user
        messages.error(request,'Usuário ou senha inválidos')
        return render(request,'accounts/login.html')
    else:
        auth.login(request,user)
        messages.success(request,'Você logou com sucesso')
        return redirect('dashboard')

    

def logout(request):
    auth.logout(request)
    return redirect('login')

def cadastro(request):
    #messages.success(request,'Olá work')
    if request.method != 'POST':
        messages.info(request,'NADA POSTADO')
        return render(request,'accounts/cadastro.html')
    
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request,'Nenhum campo pode estar vazio!')


    try:
        validate_email(email)
    except:
        messages.error(request,'Email inválido')
        return render(request,'accounts/cadastro.html')
    
    if len(senha) < 6:
        messages.error(request,"A senha deve ter no mínimo 6 caracteres")
        return render(request,'accounts/cadastro.html')

    if senha != senha2:
        messages.error(request,"Utilize a mesma senha para confirmar")
        return render(request,'accounts/cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request,'Usuário já existe')
        return render(request,'accounts/cadastro.html')
    
    if User.objects.filter(email=email).exists():
        messages.error(request,'Email já existe')
        return render(request,'accounts/cadastro.html')

    messages.success(request,'Registrado com Sucesso')
    user = User.objects.create_user(username=usuario,email=email,password=senha,first_name=nome,last_name=sobrenome) #Cadastrado no admin
    return redirect('login')

@login_required(redirect_field_name='login') # apenas se estiver logado, do contrário redireciona para a página de login
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request,'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)

    #validando com métodos do django
    if  not form.is_valid():
        messages.error(request,'Erro ao enviar formulário')
        form = FormContato(request.POST)
        return render(request,'accounts/dashboard.html',{'form':form})
    
    #Fazer uma validação na mão
    descricao = request.POST.get('descricao')
    if len(descricao < 5):
        messages.error(request,'Descrição precisa de mais caracteres')
        form = FormContato(request.POST)
        return render(request,'accounts/dashboard.html',{'form':form})

    form.save() #Precisa salvar
    messages.success(request,f'Contato {request.POST.get("nome")} salvo com sucesso')
    return redirect('dashboard')