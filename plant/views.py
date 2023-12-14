from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import MashinsListForm, ProblemsForm, LoginUserForm, DTOForm
from .models import Ceh, MashinsList, Problems, DTO

list_ceh = []


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('data')


@login_required()
def data(request):
    mashinslist = MashinsList.objects.all()
    data = {
        'MashinsList': mashinslist
    }
    return render(request, "plant/data.html", data)


# @login_required()
# def update(request):
#     if request.method == 'POST':
#         form = MashinsListForm(request.POST)
#     else:
#         form = MashinsListForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'plant/add_data.html', context)


@login_required()
def problems(request):
    problems = Problems.objects.all()
    data = {
        'Problems': problems
    }
    return render(request, "plant/problems.html", data)


@login_required()
def dto(request):
    dto = DTO.objects.all()
    data = {
        'DTO': dto,
    }
    return render(request, "plant/dto.html", data)


@login_required()
def data_slug(request, cat_slug):
    ceh = Ceh.objects.all()
    for n in ceh:
        list_ceh.append(str(n))
    if cat_slug in list_ceh:
        mashins = MashinsList.objects.filter(ceh__contains=cat_slug)
        list_ceh.clear()
        data = {
            'cat_slug': cat_slug,
            'MashinsList': mashins,
        }
        return render(request, "plant/data.html", data)
    else:
        list_ceh.clear()
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@login_required()
def problems_slug(request, cat_slug):
    ceh = Ceh.objects.all()
    for n in ceh:
        list_ceh.append(str(n))
    if cat_slug in list_ceh:
        problems = Problems.objects.filter(ceh__contains=cat_slug)
        list_ceh.clear()
        data = {
            'cat_slug': cat_slug,
            'Problems': problems
        }
        return render(request, "plant/problems.html", data)
    else:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@login_required()
def dto_slug(request, cat_slug):
    ceh = Ceh.objects.all()
    for n in ceh:
        list_ceh.append(str(n))
    if cat_slug in list_ceh:
        dto = DTO.objects.filter(ceh__contains=cat_slug)
        list_ceh.clear()
        data = {
            'cat_slug': cat_slug,
            'DTO': dto
        }
        return render(request, "plant/dto.html", data)
    else:
        return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@login_required()
def add_data(request):
    if request.method == 'POST':
        form = MashinsListForm(request.POST)
        if form.is_valid():
            MashinsList.objects.create(**form.cleaned_data)
            return redirect('data')
    else:
        form = MashinsListForm()
    context = {
        'form': form,
        'title': 'Добавление оборудования'
    }
    return render(request, 'plant/add_data.html', context)


@login_required()
def add_dto(request):
    if request.method == 'POST':
        form = DTOForm(request.POST, request.FILES)
        if form.is_valid():
            # f = DTO(files=form.cleaned_data['file'])
            # f.save()
            DTO.objects.create(**form.cleaned_data)
            return redirect('dto')
    else:
        form = DTOForm()
    context = {
        'form': form,
        'title': 'Добавление карты ДТО'
    }
    return render(request, 'plant/add_dto.html', context)


class UpdateDTO(UpdateView):
    model = DTO
    fields = ['number', 'name_mashine', 'ceh', 'start_date', 'document', 'responsible', 'comment', 'status']
    template_name = 'plant/add_dto.html'
    success_url = reverse_lazy('dto')
    title_page = 'Редактирование карты ДТО'


class UpdateMashinsList(UpdateView):
    model = MashinsList
    fields = ['number', 'name_mashine', 'ceh', 'register_date', 'manufacturer', 'number_plant', 'build_date',
              'status', 'characteristics']
    template_name = 'plant/add_data.html'
    success_url = reverse_lazy('data')
    title_page = 'Редактирование характеристик оборудования'


class UpdateProblems(UpdateView):
    model = Problems
    fields = ['number', 'name_mashine', 'ceh', 'start_date', 'description', 'comp_work', 'spare_parts', 'status',
              'finish_date', 'responsible', 'comment']
    template_name = 'plant/add_problems.html'
    success_url = reverse_lazy('problems')
    title_page = 'Редактирование неполадок оборудования'


@login_required()
def add_problems(request):
    if request.method == 'POST':
        form = ProblemsForm(request.POST)
        if form.is_valid():
            Problems.objects.create(**form.cleaned_data)
            return redirect('problems')
    else:
        form = ProblemsForm()
    context = {
        'form': form,
        'title': 'Добавление неполадки'
    }
    return render(request, 'plant/add_problems.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

