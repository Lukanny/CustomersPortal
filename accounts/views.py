from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages, auth
from django.contrib.auth import logout, views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from customers.models import Empresa, Representante
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


        if not Empresa.objects.filter(nome_fantasia_da_empresa=company_name):
                customer = Empresa.objects.create(nome_fantasia_da_empresa=company_name, endereço_da_empresa=company_adress, número_de_telefone_da_empresa=company_number, email_da_empresa=company_email)
                customer.save()
                if User.objects.filter(username=username):
                    messages.error(request, 'Usuário já em uso!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=company_email, password=password, first_name=employee.split(' ')[0], last_name=employee.split(' ')[-1])
                    user.save()
                    worker = Representante.objects.create(empresa=customer, nome_do_representante_legal=employee, rg_do_representante_legal=employee_id, cpf_do_representante_legal=employee_nif, cargo_do_representante_legal=employee_position, username=user)
                    worker.save()
                    messages.success(request, 'Conta criada, faça login na plataforma com o usuário e senha cadastrados!')
                    return redirect('login')
        if not Representante.objects.filter(nome_do_representante_legal=employee):
                if User.objects.filter(username=username):
                    messages.error(request, 'Usuário já em uso!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=company_email, password=password, first_name=employee.split(' ')[0], last_name=employee.split(' ')[-1])
                    user.save()
                    customer = Empresa.objects.get(nome_fantasia_da_empresa=company_name)
                    worker = Representante.objects.create(empresa=customer, nome_do_representante_legal=employee, rg_do_representante_legal=employee_id, cpf_do_representante_legal=employee_nif, cargo_do_representante_legal=employee_position, username=user)
                    worker.save()
                    messages.success(request, 'Conta criada, faça login na plataforma com o usuário e senha cadastrados!')
                    return redirect('login')
        messages.error(request, 'Representante legal já cadastrado!')
        return redirect('register')
    else:
        return render(request, "accounts/new_account.html")


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = 'password_reset_done'

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = 'password_reset_complete'
