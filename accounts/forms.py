from customers.models import Cliente
from django import forms


class CustomersProfileForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cargo_do_representante_legal', 'email_da_empresa', 'usuário_da_empresa']