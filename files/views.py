from django.http import HttpResponse
from customers.models import Cliente
from .models import Arquivo

def get_customer_files(request):
    if request.user.is_authenticated:
        customer = Cliente.objects.filter(usuário_da_empresa=request.user.username)
        return Arquivo.objects.filter(cliente=customer)
    else:
        return HttpResponse('User Not Authenticated!')
    