from django import forms
from .models import Instalacion, Tecnico

PLANES = [
    ['BP', 'BÁSICO PLUS'],
    ['BA', 'BÁSICO'],
    ['BR', 'BRONCE'],
    ['PL', 'PLATA'],
    ['OR', 'ORO']
]

HORAS_ESTIMADAS = [
    [1, "00:30"],
    [2, "01:00"],
    [3, "01:30"],
    [4, "02:00"],
    [5, "02:30"],
    [6, "03:00"],
    [7, "03:30"],
    [8, "04:00"],
    [9, "04:30"],
    [10, "05:00"],
    [11, "05:30"],
    [12, "06:00"],
]

PRIORIDAD = [
    [1, 'Baja'],
    [2, 'Media'],
    [3, 'Alta'],
]

class InstalacionForm(forms.ModelForm):
    nro_contrato = forms.CharField(label="Nro. de Contrato", min_length=7, max_length=7)
    nombre_cliente = forms.CharField(label="Nomble Cliente")
    direccion = forms.CharField(widget=forms.Textarea(attrs={"rows":"3"}),label="Dirección", required=False)
    numero_telefono1 = forms.CharField(label="Nro. Teléfono 1", min_length=11)
    numero_telefono2 = forms.CharField(label="Nro. Teléfono 2", min_length=11,required=False)
    prioridad = forms.ChoiceField(choices=PRIORIDAD)
    plan = forms.ChoiceField(choices=PLANES, initial='BR')
    tiempo_estimado = forms.ChoiceField(choices=HORAS_ESTIMADAS, label="Tiempo Estimado", initial=3)
    observaciones = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=False)

    class Meta:
        model = Instalacion
        fields = [
            'nro_contrato',
            'nombre_cliente',
            'direccion',
            'numero_telefono1',
            'numero_telefono2',
            'plan',
            'prioridad',
            'tiempo_estimado',
            'observaciones'
            ]

    def clean(self):
        super().clean()
        numero_telefono1 = self.cleaned_data['numero_telefono1']
        for char in numero_telefono1:
            if (char == "+"):
                break
            try: int(char)
            except:
                raise forms.ValidationError("Número de teléfono no válido")

        numero_telefono2 = self.cleaned_data['numero_telefono2']
        for char in numero_telefono2:
            if (char == "+"):
                break
            try: int(char)
            except:
                raise forms.ValidationError("Número de teléfono no válido")

        
        
    
class InstalacionUpdateForm(forms.ModelForm):
    nro_contrato = forms.CharField(label="Nro. de Contrato", min_length=7, max_length=7, required=False, disabled="disabled")
    nombre_cliente = forms.CharField(label="Nomble Cliente")
    direccion = forms.CharField(widget=forms.Textarea(attrs={"rows":"3"}),label="Dirección", required=False)
    numero_telefono1 = forms.CharField(label="Nro. Teléfono 1", min_length=11)
    numero_telefono2 = forms.CharField(label="Nro. Teléfono 2", min_length=11,required=False)
    plan = forms.ChoiceField(choices=PLANES)
    prioridad = forms.ChoiceField(choices=PRIORIDAD)
    tiempo_estimado = forms.ChoiceField(choices=HORAS_ESTIMADAS, label="Tiempo Estimado")
    observaciones = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=False)
    tecnico = forms.ModelChoiceField(Tecnico.objects.all(), widget=forms.Select(attrs={'disabled':'disabled'}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'disabled':'disabled'}, format="%Y-%m-%d"), required=False)

    class Meta:
        model = Instalacion
        fields = [
            'nro_contrato',
            'nombre_cliente',
            'direccion',
            'numero_telefono1',
            'numero_telefono2',
            'plan',
            'prioridad',
            'tiempo_estimado',
            'observaciones',
            'tecnico',
            'fecha'
            ]

    def clean(self):
        super().clean()
        numero_telefono1 = self.cleaned_data['numero_telefono1']
        for char in numero_telefono1:
            if (char == "+"):
                break
            try: int(char)
            except:
                raise forms.ValidationError("Número de teléfono no válido")

        numero_telefono2 = self.cleaned_data['numero_telefono2']
        for char in numero_telefono2:
            print(char)
            if (char == "+"):
                break
            try: int(char)
            except:
                raise forms.ValidationError("Número de teléfono no válido")
    

class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput())
