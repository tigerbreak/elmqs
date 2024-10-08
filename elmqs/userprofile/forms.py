from django import forms
from django.contrib.auth.models import User
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=30)
    password_confirm = forms.CharField(max_length=30)
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            return password
        else:
            raise forms.ValidationError("Passwords do not match")


