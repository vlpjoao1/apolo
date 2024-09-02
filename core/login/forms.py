from datetime import datetime

import requests
from django import forms
from django.contrib.auth import authenticate

from core.security.choices import LOGIN_TYPE
from core.security.models import AccessUser
from core.user.models import User


class AuthenticationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        if not username:
            raise forms.ValidationError('Ingrese un username válido.')
        elif not password:
            raise forms.ValidationError('Ingrese una contraseña válida.')
        # response_api = self.get_or_crete_user_api(user=username, password=password)
        # if not response_api.get('resp'):
        #     raise forms.ValidationError(response_api.get('msg'))
        queryset = User.objects.filter(username=username)
        if queryset.exists():
            user = queryset[0]
            if not user.is_active:
                raise forms.ValidationError('El usuario ha sido bloqueado, comuníquese con su administrador.')
            if authenticate(username=username, password=password) is None:
                AccessUser(user=user, type=LOGIN_TYPE[1][0]).save()
                int_fall = user.accessuser_set.filter(type=LOGIN_TYPE[1][0], date_joined=datetime.now().date()).count()
                if int_fall > 2:
                    user.is_active = False
                    user.save()
                    raise forms.ValidationError('El usuario ha superado el límite de intentos fallidos en un día.')
                int_res = 3 - int_fall
                raise forms.ValidationError(f"La contraseña ingresada es incorrecta, "
                                            f"le {'quedan' if int_res > 1 else 'queda'} {int_res} {'intentos' if int_res >1 else 'intento'}."
                                            f"Si supera los 3 intentos, el usuario será bloqueado.")
            AccessUser(user=user).save()
            return cleaned_data
        raise forms.ValidationError('Por favor introduzca el nombre de usuario y la clave'
                                    ' correctos para una cuenta de personal. Observe que '
                                    'ambos campos pueden ser sensibles a mayúsculas.')

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)

    def get_or_crete_user_api(self, user, password):
        response = {'resp': False, 'msg': 'No se ha podido iniciar sesión '}
        try:
            payload = {
                'username': user,
                'password': password,
            }
            headers = {
                'Authorization': 'Token 09fcedfbb892e398b850da5877216cca94a5fe68'
            }
            r = requests.post('http://localhost:8000/api/login/', data=payload, headers=headers)
            if r.status_code == 200:
                response = r.json()
                if response['resp']:  # Resp return True/False
                    queryset = User.objects.filter(username=response['user']['username'])
                    if not queryset.exists():  # Create in local db if not exists
                        """Creamos el usuario porque el método login()
                        debe recibir una instancia de usuario, y al usar el 
                        get_user en LoginAPIView, se busca el usuario en la DB"""
                        user = User()
                        user.username = response['user']['username']
                        user.first_name = response['user']['first_name']
                        user.last_name = response['user']['last_name']
                        user.email = response['user']['email']
                        user.set_password(response['user']['username'])
                        user.is_superuser = True
                        user.is_staff = True
                        user.save()
            else:
                response['msg'] = r.text
        except Exception as e:
            response['msg'] = str(e)
        return response


class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese un username',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        if not User.objects.filter(username=cleaned['username']).exists():
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('El usuario no existe')
        return cleaned

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            # self._errors['error'] = self._errors.get('error', self.error_class())
            # self._errors['error'].append('El usuario no existe')
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
