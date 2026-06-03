from django import forms
from .models import Frequencia


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = ['aluno', 'turma', 'data', 'status', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'turma': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.RadioSelect(),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ChamadaDiariaForm(forms.Form):
    """Form for batch daily attendance marking"""
    turma = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        label='Turma',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    data = forms.DateField(
        label='Data',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        from escola.models import Turma
        super().__init__(*args, **kwargs)
        self.fields['turma'].queryset = Turma.objects.filter(ativo=True)


class FrequenciaInlineForm(forms.Form):
    """Form for marking attendance for a single student"""
    status = forms.ChoiceField(
        choices=Frequencia.Status.choices,
        widget=forms.RadioSelect(),
        required=False
    )
    observacoes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False
    )
