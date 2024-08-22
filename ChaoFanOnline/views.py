from django.db.models.base import Model as Model

from django.shortcuts import render,get_object_or_404

from django import forms
from ckeditor.fields import RichTextFormField
from markdownx.fields import MarkdownxFormField

from django.http import HttpResponseRedirect

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

from django.contrib.auth.models import User

#用户注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, help_text="Enter a username (20 characters max).")
    email = forms.EmailField(help_text="Enter a valid email address.")
    password1 = forms.CharField(widget=forms.PasswordInput, help_text="Enter a password (8 characters min).")
    password2 = forms.CharField(widget=forms.PasswordInput, help_text="Enter the same password as above.")
    
    def clean_email(self):
        data = self.cleaned_data['email']
        #检查该字段是否是一个合法的email地址
        if not '@' in data:
            raise ValidationError(_('Invalid email address'))
     
        return data

    def clean_username(self):
        data = self.cleaned_data['username']

        #Check username is not already taken.
        if User.objects.filter(username=data).exists():
            raise ValidationError(_('Username already taken'))

        # Remember to always return the cleaned data.
        return data

    #自定义clean方法，检查两次输入的密码是否一致
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords do not match'))
        return cleaned_data


def UserCreate(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(user_name, email, password)
            user.groups.add(1)
            user.save()
            #重定向至accounts/login页面
            return HttpResponseRedirect('/accounts/login/')
        else:
            return render(request, 'registration/register.html', {'form': form})
            
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
