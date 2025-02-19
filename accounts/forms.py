from customers.models import Representante
from django import forms


class CustomersProfileForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['cargo', 'email', 'username']