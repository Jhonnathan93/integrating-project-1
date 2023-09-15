from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField


class UserCreateForm(UserCreationForm):
    name = forms.CharField(max_length=45, required=True, label='Nombre completo')
    email = forms.EmailField(max_length=45, required=True, label='Correo electrónico')
    birthdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Fecha de nacimiento'
    )
    captcha = ReCaptchaField(
        label='Captcha',
        required=True,
    )
    profilePic = forms.ImageField(label='Foto de Perfil', required=False)


    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        data = ['name', 'email', 'birthdate', 'username', 'password1', 'password2']

        for fieldname in data:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})
