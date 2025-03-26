from django import forms
from .models import News
from django.contrib.auth.models import User


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']
class SignUpForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']