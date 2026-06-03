from django import forms
from .models import Aluno, Matricula


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'data_nascimento', 'responsavel', 'telefone', 'email', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class MatriculaForm(forms.ModelForm):
    class Meta:
        model = Matricula
        fields = ['aluno', 'turma', 'status', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
