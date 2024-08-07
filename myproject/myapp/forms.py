from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Servidores

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Por favor, introduzca un nombre de usuario y contraseña correctos. Por favor, note que ambos campos son sensibles a mayúsculas.",
        'inactive': "Esta cuenta está inactiva.",
    }


class LoginForm(forms.Form):
    username = forms.CharField(label="username", required=False)
    password = forms.CharField(label="password", widget=forms.PasswordInput, required=False)

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Entrar'))


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2']
    
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
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
        model = Servidores
        fields = ['DireccionIp', 'Usuario', 'Contrasena', 'Servicio', 'Puerto', 'RutaImportante', 'UbicacionFisica', 'NumeroSerie']
