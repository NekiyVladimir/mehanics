from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from .models import Ceh, DTO, Problems, MashinsList


class MashinsListForm(forms.ModelForm):
    class Meta:
        model = MashinsList
        fields = ['number', 'name_mashine', 'ceh', 'register_date', 'manufacturer', 'number_plant', 'build_date',
                  'status', 'characteristics']


# class MashinsListForm(forms.Form):
#     number = forms.CharField(label='Инв.№')
#     name_mashine = forms.CharField(label='Наименование оборудования')
#     ceh = forms.CharField(label='Выберите цех')
#     # ceh = forms.ModelChoiceField(queryset=Ceh.objects.all(), label='Цех', empty_label='Выберите цех')
#     register_date = forms.CharField(label='Дата ввода в эксплуатацию')
#     manufacturer = forms.CharField(label='Изготовитель', required=False)
#     number_plant = forms.CharField(label='Заводской номер', required=False)
#     build_date = forms.IntegerField(label='Дата изготовления', required=False)
#     characteristics = forms.CharField(label='Характеристики оборудования')


class ProblemsForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['number', 'name_mashine', 'ceh', 'start_date', 'description', 'comp_work', 'spare_parts', 'status',
                  'finish_date', 'responsible', 'comment']


# class ProblemsForm(forms.Form):
#     number = forms.CharField(max_length=10, label='Инв.№')
#     name_mashine = forms.CharField(max_length=300, label='Наименование оборудования')
#     ceh = forms.ModelChoiceField(queryset=Ceh.objects.all(), label='Цех', empty_label='Выберите цех')
#     start_date = forms.DateField(label='Дата выявления неполадки')
#     description = forms.CharField(label='Описание неполадки')
#     comp_work = forms.CharField(label='Выполненые работы', required=False)
#     spare_parts = forms.CharField(max_length=300, label='Запчасти', required=False)
#     status = forms.CharField(max_length=50, label='Статус', required=False)
#     finish_date = forms.DateField(label='Дата устранения неполадки', required=False)
#     responsible = forms.CharField(max_length=50, label='Отвественный', required=False)
#     comment = forms.CharField(label='Комментарий',  required=False)
#     pub_date = forms.DateTimeField(label='Дата публикации', required=False)


class DTOForm(forms.ModelForm):
    class Meta:
        model = DTO
        fields = ['number', 'name_mashine', 'ceh', 'start_date', 'document', 'responsible', 'status', 'comment']


# class DTOForm(forms.Form):
#     number = forms.CharField(max_length=30, label='Инв.№')
#     name_mashine = forms.CharField(max_length=300, label='Наименование оборудования')
#     ceh = forms.CharField(label='Выберите цех')
#     # ceh = forms.ModelChoiceField(queryset=Ceh.objects.all(), label='Цех', empty_label='Выберите цех')
#     start_date = forms.DateField(label='Дата проведения ДТО')
#     document = forms.FileField(label='Скан документов')
#     responsible = forms.CharField(max_length=50, label='Ответственный', required=False)
#     comment = forms.CharField(label='Комментарий',  required=False)
#     pub_date = forms.DateTimeField(label='Дата публикации', required=False)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
