from django import forms
from .models import Representante


class RepresentanteForm(forms.ModelForm):
    cnpj_da_empresa = forms.CharField(
        max_length=12, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-md bg-light fs-6 text-dark',
            'readonly': 'readonly',
        })
    )
    class Meta:
        model = Representante
        fields = ['nome_do_representante_legal', 'cpf_do_representante_legal', 'cargo_do_representante_legal', 'email_do_representante_legal', 'cnpj_da_empresa']
    
    def __init__(self, *args, **kwargs) -> None:
        super(RepresentanteForm, self).__init__(*args, **kwargs)
        self.fields['nome_do_representante_legal'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
        self.fields['nome_do_representante_legal'].widget.attrs['readonly'] = True
        self.fields['nome_do_representante_legal'].label = "Nome"


        self.fields['cpf_do_representante_legal'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
        self.fields['cpf_do_representante_legal'].widget.attrs['readonly'] = True
        self.fields['cpf_do_representante_legal'].label = "CPF"

        self.fields['cargo_do_representante_legal'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
        self.fields['cargo_do_representante_legal'].label = "Cargo Atual"

        if self.instance and self.instance.cnpj_da_empresa:
            self.fields['cnpj_da_empresa'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
            self.fields['cnpj_da_empresa'].label = "CNPJ da Empresa"

        self.fields['email_do_representante_legal'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
        self.fields['email_do_representante_legal'].label = "E-mail Administrativo"
