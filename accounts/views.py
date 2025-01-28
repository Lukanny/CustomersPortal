from django.contrib import messages, auth
from django.contrib.auth import logout, views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse
from customers.models import Empresa, Endereço, Representante
from customers.forms import RepresentanteForm
from string import punctuation

@login_required
def dashboard(request):
    try:
        worker = Representante.objects.get(username__username=request.user.username)
        company = worker.empresa
        files = company.files.all()
        return render(request, "accounts/dashboard.html", {'files':files, 'worker':worker})
    except Representante.DoesNotExist:
        return HttpResponse('<h1>Não há um representante cadastrado, por favor, contatar o suporte.</h1>')


@login_required
def change_user_info(request):
    worker = Representante.objects.get(username__username=request.user.username)
    if request.method == 'POST':
        form = RepresentanteForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mudanças salvas com sucesso!')
    else:
        form = RepresentanteForm(instance=worker)
    return render(request, "accounts/change_user_info.html",  {'form': form, 'worker': worker})

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

import re
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def is_valid_cpf(cpf):
    """Valida o CPF"""
    cpf = re.sub(r'\D', '', cpf)  # Remove tudo que não for número
    if len(cpf) != 11 or not cpf.isdigit() or cpf in (c * 11 for c in "1234567890"):
        return False
    # Calcula os dígitos verificadores
    for i in range(9, 11):
        value = sum((int(cpf[num]) * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != int(cpf[i]):
            return False
    return True

def is_valid_cnpj(cnpj):
    """Valida o CNPJ"""
    cnpj = re.sub(r'\D', '', cnpj)  # Remove tudo que não for número
    if len(cnpj) != 14 or not cnpj.isdigit():
        return False
    # Calcula os dígitos verificadores
    return True

def register(request):
    if request.method == "POST":
        # Dados do formulário
        employee = request.POST['empregado_nome']
        employee_nif = request.POST['empregado_cpf']
        employee_position = request.POST['empregado_cargo']
        employee_email = request.POST['email_funcionario']
        confirm_employee_email = request.POST['email_funcionario2']
        company_name = request.POST['nome_empresa']
        company_nif = request.POST['cnpj_empresa']
        street = request.POST['endereco_rua']
        neighborhood = request.POST['endereco_bairro']
        number = request.POST['endereco_numero']
        zip_code = request.POST['endereco_cep']
        city = request.POST['endereco_cidade']
        state = request.POST['endereco_estado']
        phone = request.POST['telefone_empresa']
        username = request.POST['usuario']
        password = request.POST['senha']
        confirm_password = request.POST['senha2']
        
        # Validações
        if not is_valid_cpf(employee_nif):
            messages.error(request, 'CPF inválido!')
            return redirect('register')
        if not is_valid_cnpj(company_nif):
            messages.error(request, 'CNPJ inválido!')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'As senhas informadas não são iguais!')
            return redirect('register')
        if len(password) < 8:
            messages.error(request, 'A senha deve conter no mínimo 8 caracteres!')
            return redirect('register')
        if not any(ch.isdigit() for ch in password) or not any(c in punctuation for c in password):
            messages.error(request, 'A senha deve conter letras, números e símbolos especiais!')
            return redirect('register')
        if employee_email != confirm_employee_email:
            messages.error(request, 'Os e-mails informados não são iguais!')
            return redirect('register')
        try:
            validate_email(employee_email)
        except ValidationError:
            messages.error(request, 'E-mail inválido!')
            return redirect('register')
        if not zip_code.isdigit() or len(zip_code) != 8:
            messages.error(request, 'CEP inválido! Certifique-se de inserir apenas números.')
            return redirect('register')
        if not phone.isdigit() or len(phone) < 10:
            messages.error(request, 'Telefone inválido! Certifique-se de inserir um número com DDD.')
            return redirect('register')

        try:
            with transaction.atomic():
                # Criação da empresa e endereço
                empresa, created = Empresa.objects.get_or_create(
                    nome_fantasia_da_empresa=company_name,
                    cnpj_da_empresa=company_nif,
                    defaults={
                        'número_de_telefone_da_empresa': phone,
                    }
                )
                if created:
                    endereco = Endereço.objects.create(
                        rua=street,
                        bairro=neighborhood,
                        número=number,
                        cep=zip_code,
                        cidade=city,
                        estado=state
                    )
                    empresa.endereço_da_empresa = endereco
                    empresa.save()

                # Verifica se o representante já está cadastrado
                if Representante.objects.filter(cpf_do_representante_legal=employee_nif).exists():
                    messages.error(request, 'Representante legal já cadastrado!')
                    return redirect('register')

                # Verifica se o nome de usuário já está em uso
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Usuário já em uso!')
                    return redirect('register')

                # Cria o usuário
                user = User.objects.create_user(
                    username=username,
                    email=employee_email,
                    password=password,
                    first_name=employee.split(' ')[0],
                    last_name=employee.split(' ')[-1]
                )

                # Cria o representante
                Representante.objects.create(
                    empresa=empresa,
                    nome_do_representante_legal=employee,
                    cpf_do_representante_legal=employee_nif,
                    cargo_do_representante_legal=employee_position,
                    email_do_representante_legal=employee_email,
                    username=user
                )

                messages.success(request, 'Conta criada com sucesso! Faça login na plataforma.')
                return redirect('login')

        except Exception as e:
            messages.error(request, f'Ocorreu um erro durante o cadastro: {str(e)}')
            return redirect('register')

    return render(request, "accounts/new_account.html")


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = 'password_reset_done'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = 'password_reset_complete'
