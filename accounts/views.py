from django.shortcuts import render, redirect

def dashboard(request):
    return render(request, "accounts/dashboard.html")

def login(request):
    return render(request, "accounts/login.html")

def logout(request):
    return redirect('index')

def forgot_password(request):
    return render(request, "accounts/forgot_password.html")

def register(request):
    return render(request, "accounts/new_account.html")
