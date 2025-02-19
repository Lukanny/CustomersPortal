from django.contrib import messages, auth
from django.contrib.auth import logout, views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.db import transaction
from django.shortcuts import render, redirect, HttpResponse
from customers.models import Empresa, Endereco, Representante
from customers.forms import RepresentanteForm
from string import punctuation

import re
import uuid

@login_required
def dashboard(request):
    try:
        worker = Representante.objects.get(username__username=request.user.username)
        company = worker.empresa
        files = company.files.all()
        return render(request, "accounts/dashboard.html", {'files': files, 'worker': worker})
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

        # Validations (Your existing validations)
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
                # 1. Get or create the Endereco (Your existing logic)
                endereco, endereco_created = Endereco.objects.get_or_create(
                    rua=street,
                    bairro=neighborhood,
                    numero=number,
                    cep=zip_code,
                    cidade=city,
                    estado=state,
                    defaults={}
                )

                # 2. Get or create the Empresa (Your existing logic)
                empresa, empresa_created = Empresa.objects.get_or_create(
                    cnpj=company_nif,
                    defaults={
                        'nome_fantasia': company_name,
                        'telefone': phone,
                        'endereco': endereco,
                    }
                )

                if not empresa_created and empresa.endereco != endereco:
                    empresa.endereco = endereco
                    empresa.save()

                if Representante.objects.filter(cpf=employee_nif).exists():
                    messages.error(request, 'Representante legal já cadastrado!')
                    return redirect('register')

                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Usuário já em uso!')
                    return redirect('register')

                # 3. Create the User (Modified)
                user = User.objects.create_user(
                    username=username,
                    email=employee_email,
                    password=password,
                    first_name=employee.split(' ')[0],
                    last_name=employee.split(' ')[-1]
                )
                user.is_active = False  # Deactivate the user
                user.save()

                # 4. Create the Representante (Modified)
                representante = Representante.objects.create(
                    empresa=empresa,
                    nome=employee,
                    cpf=employee_nif,
                    cargo=employee_position,
                    email=employee_email,
                    username=user  # Link to the User
                )

                # 5. Generate and store token (New)
                token = str(uuid.uuid4())
                representante.activation_token = token
                representante.save()

                # 6. Send verification email using Django's default email functions
                send_verification_email(representante, user, token)

                messages.success(request, 'Conta criada com sucesso! Verifique seu e-mail para ativar sua conta.')
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


def send_verification_email(representante, user, token):
    subject = "Ative sua conta PROSESMT"
    from_email = "your_verified_email@example.com"  # Use your verified email address (or DEFAULT_FROM_EMAIL from settings)
    activation_link = f"https://yourdomain.com/activate/?token={token}"  # Activation link

    html_content = f"""
    <html>
    <body>
        <p>Olá {representante.nome},</p>
        <p>Obrigado por se registrar no PROSESMT. Clique no link abaixo para ativar sua conta:</p>
        <p><a href="{activation_link}">{activation_link}</a></p>
    </body>
    </html>
    """

    text_content = f"Olá {representante.nome},\n\nObrigado por se registrar no PROSESMT. Clique no link abaixo para ativar sua conta:\n\n{activation_link}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, [representante.email])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        # Log the error as needed

def activate(request):
    token = request.GET.get('token')
    if token:
        try:
            representante = Representante.objects.get(activation_token=token)
            user = representante.username  # Get the related User object
            user.is_active = True
            user.save()
            representante.activation_token = None
            representante.save()
            messages.success(request, "Conta ativada com sucesso!")
            return redirect('login')  # Redirect to the login page
        except Representante.DoesNotExist:
            messages.error(request, "Token de ativação inválido.")
            return redirect('register')  # Or any other appropriate page
    else:
        messages.error(request, "Nenhum token de ativação fornecido.")
        return redirect('register')  # Or any other appropriate page
