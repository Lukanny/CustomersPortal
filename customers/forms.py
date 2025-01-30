from django import forms
from .models import Representante


class RepresentanteForm(forms.ModelForm):
    cnpj = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-md fs-6 text-light',
            'readonly': 'readonly',
            'style': 'background-color: #343a40;',
        })
    )
    nome_fantasia = forms.CharField(
        max_length=254,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-md fs-6 text-light',
            'readonly': 'readonly',
            'style': 'background-color: #343a40;',
        }),
        label="Nome da Empresa"
    )

    class Meta:
        model = Representante
        fields = [
            'nome',
            'cpf',
            'cargo',
            'email',
            'nome_fantasia',
            'cnpj',
        ]

    def __init__(self, *args, **kwargs) -> None:
        super(RepresentanteForm, self).__init__(*args, **kwargs)

        readonly_fields = [
            'nome',
            'cpf',
            'nome_fantasia',
            'cnpj',
        ]

        for field in readonly_fields:
            self.fields[field].widget.attrs.update({
                'readonly': True,
                'class': 'form-control form-control-md fs-6 text-light',
                'style': 'background-color: #343a40;'
            })

        if self.instance and self.instance.empresa:
            self.fields['cnpj'].initial = self.instance.empresa.cnpj
            self.fields['nome_fantasia'].initial = self.instance.empresa.nome_fantasia

        self.fields['cargo'].widget.attrs.update({
            'class': 'form-control form-control-md fs-6 text-dark bg-light',
        })
        self.fields['cargo'].label = "Cargo Atual"

        self.fields['email'].widget.attrs.update({
            'class': 'form-control form-control-md fs-6 text-dark bg-light',
        })
        self.fields['email'].label = "E-mail Administrativo"
