from django import forms
from .models import Serie, Disciplina, Turma, Professor


class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: 1º Ano'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nome', 'codigo', 'descricao', 'carga_horaria', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: MAT001'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'serie', 'ano', 'periodo', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ex: A'}),
            'serie': forms.Select(attrs={'class': 'form-control'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ['numero_registro', 'telefone', 'disciplinas', 'turmas', 'ativo']
        widgets = {
            'numero_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'disciplinas': forms.CheckboxSelectMultiple(),
            'turmas': forms.CheckboxSelectMultiple(),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
