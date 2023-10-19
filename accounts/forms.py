from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import userInformation

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = userInformation
        fields = ('birthdate', 'preferences', 'profile_picture')
    
    # Add User model fields to the form
    username = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)


from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField

class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    email = forms.EmailField(
        max_length=45,
        required=True,
        label='Email',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    birthdate = forms.DateField(
        required=True,
        label='Fecha de nacimiento',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    preferences = forms.CharField(
        max_length=300,
        required=True,
        label='Escribe lo que te interese en la lectura',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        label='Foto de Perfil',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    captcha = ReCaptchaField(
        label='Captcha',
        required=True
    )
    

from django.contrib.auth.forms import AuthenticationForm

class loginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))