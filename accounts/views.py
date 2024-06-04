from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customers.models import Cliente
from string import punctuation

@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def login(request):
    if request.method == "POST":
        username = request.POST['usuario']
        password = request.POST['senha']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuário e/ou senha incorretos!")
            return redirect('login')
    else:
        return render(request, "accounts/login.html")

def custom_logout(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        #logic
        return
    else:
        return render(request, "accounts/forgot_password.html")

def register(request):
    if request.method == "POST":
        employee = request.POST['empregado_nome']
        employee_id = request.POST['empregado_rg']
        employee_nif = request.POST['empregado_cpf']
        employee_position = request.POST['empregado_cargo']
        company_name = request.POST['nome_empresa']
        company_adress = request.POST['endereco_empresa']
        company_number = request.POST['telefone_empresa']
        company_email = request.POST['email_empresa']
        confirm_company_email = request.POST['email_empresa2']
        username = request.POST['usuario']
        password = request.POST['senha']
        confirm_password = request.POST['senha2']
        
        if not password == confirm_password:
            messages.error(request, 'As senhas informadas não são iguais!')
            return redirect('register')
        if not len(password) >= 8:
            messages.error(request, 'A senha deve conter no mínimo 8 caracteres!')
            return redirect('register')
        if not any(ch.isdigit() for ch in password) or not any(c in punctuation for c in password):
            messages.error(request, 'A senha deve conter letras e números!')
            return redirect('register')
        if not company_email == confirm_company_email:
            messages.error(request, 'Os e-mails informados não são iguais!')
            return redirect('register')
        if not Cliente.objects.filter(nome_fantasia_da_empresa=company_name):
                customer = Cliente.objects.create(nome_do_representante_legal=employee, rg_do_representante_legal=employee_id, cpf_do_representante_legal=employee_nif, cargo_do_representante_legal=employee_position, 
                                        nome_fantasia_da_empresa=company_name, endereço_da_empresa=company_adress, número_de_telefone_da_empresa=company_number, email_da_empresa=company_email)
                customer.save()
                if not User.objects.filter(username=username):
                    user = User.objects.create_user(username=username, email=company_email, password=password)
                    user.save()
                    messages.success(request, 'Conta criada, faça login na plataforma com o usuário e senha cadastrados!')
                    return redirect('login')
                messages.error(request, 'Usuário já em uso!')
                return redirect('register')
        if not Cliente.objects.filter(nome_do_representante_legal=employee):
            if not User.objects.filter(username=username):
                user = User.objects.create_user(username=username, email=company_email, password=password)
                user.save()
                messages.success(request, 'Conta criada, faça login na plataforma com o usuário e senha cadastrados!')
                return redirect('login')
            messages.error(request, 'Usuário já em uso!')
            return redirect('register')
        messages.error(request, 'Representante legal já cadastrado!')
        return redirect('register')
    else:
        return render(request, "accounts/new_account.html")
