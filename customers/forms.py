from django import forms
from .models import Representante


class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = ['nome_do_representante_legal', 'cpf_do_representante_legal', 'cargo_do_representante_legal', 'email_do_representante_legal']
    
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

        self.fields['email_do_representante_legal'].widget.attrs.update({'class': 'form-control form-control-md bg-light fs-6 text-dark'})
        self.fields['email_do_representante_legal'].label = "E-mail Administrativo"
