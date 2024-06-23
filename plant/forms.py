from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import TextInput, Textarea

from .models import DTO, Problems, MashinsList


class MashinsListForm(forms.ModelForm):
    class Meta:
        model = MashinsList
        fields = ['number', 'name_mashine', 'ceh', 'manufacturer', 'number_plant', 'build_date', 'register_date',
                  'form', 'to', 'photo', 'nameplate', 'status', 'characteristics']
        widgets = {
            "name_mashine": TextInput(attrs={
                'style': 'width:70%;',
                # 'size': 70,
            }),
            "characteristics": Textarea(attrs={
                # 'cols': 80,
                'style': 'width:70%;',
                'rows': 10,
            })
        }


class ProblemsFormMaster(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['number', 'name_mashine', 'ceh', 'start_date', 'description', 'comp_work', 'photo_problem',
                  'spare_parts', 'status', 'finish_date', 'responsible', 'comment']
        widgets = {
            "name_mashine": TextInput(attrs={
                'style': 'width:70%;',
            }),
            "description": Textarea(attrs={
                'style': 'width:70%;',
                'rows': 5,
            }),
            "comp_work": Textarea(attrs={
                'style': 'width:70%;',
                'rows': 5,
            })
        }


class ProblemsFormUser(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['number', 'start_date', 'description', 'comp_work', 'photo_problem', 'spare_parts',
                  'status', 'finish_date', 'responsible']
        widgets = {
            "name_mashine": TextInput(attrs={
                'style': 'width:70%;',
            }),
            "description": Textarea(attrs={
                'style': 'width:70%;',
                'rows': 5,
            }),
            "comp_work": Textarea(attrs={
                'style': 'width:70%;',
                'rows': 5,
            })
        }


class DTOForm(forms.ModelForm):
    class Meta:
        model = DTO
        fields = ['number', 'start_date', 'finish_date', 'next_to', 'document',
                  'responsible', 'status', 'comment']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'style': 'margin-left: 20px;'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'style': 'margin-left: 11px;'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
