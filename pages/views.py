from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'pages/index.html')

def login(request):
    return render(request, 'pages/login.html')

def new_account(request):
    return render(request, 'pages/new_account.html')

def forgot_password(request):
    return render(request, 'pages/forgot_password.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')
