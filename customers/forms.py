from django import forms
from .models import Representante


class RepresentanteForm(forms.ModelForm):
    cnpj_da_empresa = forms.CharField(
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-md fs-6 text-light',
            'readonly': 'readonly',
            'style': 'background-color: #343a40;',
        })
    )
    nome_fantasia_da_empresa = forms.CharField(
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
            'nome_do_representante_legal',
            'cpf_do_representante_legal',
            'cargo_do_representante_legal',
            'email_do_representante_legal',
            'nome_fantasia_da_empresa',
            'cnpj_da_empresa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        super(RepresentanteForm, self).__init__(*args, **kwargs)

        readonly_fields = [
            'nome_do_representante_legal',
            'cpf_do_representante_legal',
            'nome_fantasia_da_empresa',
            'cnpj_da_empresa',
        ]

        for field in readonly_fields:
            self.fields[field].widget.attrs.update({
                'readonly': True,
                'class': 'form-control form-control-md fs-6 text-light',
                'style': 'background-color: #343a40;'
            })

        if self.instance and self.instance.empresa:
            self.fields['cnpj_da_empresa'].initial = self.instance.empresa.cnpj_da_empresa
            self.fields['nome_fantasia_da_empresa'].initial = self.instance.empresa.nome_fantasia_da_empresa

        self.fields['cargo_do_representante_legal'].widget.attrs.update({
            'class': 'form-control form-control-md fs-6 text-dark bg-light',
        })
        self.fields['cargo_do_representante_legal'].label = "Cargo Atual"

        self.fields['email_do_representante_legal'].widget.attrs.update({
            'class': 'form-control form-control-md fs-6 text-dark bg-light',
        })
        self.fields['email_do_representante_legal'].label = "E-mail Administrativo"
