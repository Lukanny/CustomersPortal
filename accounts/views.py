from django.shortcuts import render, redirect
from django.contrib import messages

def dashboard(request):
    return render(request, "accounts/dashboard.html")

def login(request):
    if request.method == "POST":
        #logic
        return
    else:
        return render(request, "accounts/login.html")

def logout(request):
    return redirect('index')

def forgot_password(request):
    if request.method == "POST":
        #logic
        return
    else:
        return render(request, "accounts/forgot_password.html")

def register(request):
    if request.method == "POST":
        #logic
        messages.error(request, 'Testing error message')
        return redirect('register')
    else:
        return render(request, "accounts/new_account.html")
