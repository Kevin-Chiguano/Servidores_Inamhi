from django import forms
from .models import MyModel, CambioCustodio
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Por favor, introduzca un nombre de usuario y contraseña correctos. Por favor, note que ambos campos son sensibles a mayúsculas.",
        'inactive': "Esta cuenta está inactiva.",
    }


class LoginForm(forms.Form):
    username = forms.CharField(label="username", required=False)
    password = forms.CharField(label="password", widget=forms.PasswordInput, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Entrar'))


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('register','Register'))
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            viewers_group = Group.objects.get(name='viewers')
            user.groups.add(viewers_group)
            return User


class MyModelForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['codigo_tic','codigo_bien', 'codigo_anterior', 'codigo_provisional', 'codigo_nuevo', 'nombre_bien', 
                  'serie', 'modelo', 'marca', 'color', 'material', 'estado', 'ubicacion', 'cedula', 
                  'custodio_actual', 'observacion', 'archivo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # Si el registro no existe (es decir, estamos en la creación)
            # Si el registro no existe (es decir, estamos en la creación)
            for field_name in self.fields:
                if field_name != 'archivo':
                    self.fields[field_name].required = False



class CambioCustodioForm(forms.ModelForm):
    class Meta:
        model = CambioCustodio
        fields = ['nuevo_custodio', 'cedula_nuevo_custodio']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk is None:  # Si el registro no existe (es decir, estamos en la creación)
            # Si el registro no existe (es decir, estamos en la creación)
            for field_name in self.fields:
                self.fields[field_name].required = False
