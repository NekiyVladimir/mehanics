import hashlib
from datetime import date
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
import requests
import json
from django.forms import TextInput, Textarea
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import MashinsListForm, LoginUserForm, DTOForm, ProblemsFormMaster, ProblemsFormUser
from .models import MashinsList, Problems, DTO, UserGroup

list_ceh = []


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('data')


@login_required()
def data(request):
    if request.user.username:
        name = request.user.username
        print(request.user.id)
        print(name)
        name_mashine = request.POST.get("name_mashine", 'Null')
        number = request.POST.get("number", 'Null')
        workgroup = request.POST.get("workgroup", 'Null')
        sort = request.POST.get("sort", 'pk')
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
            ceh = cat_slug
            if cat_slug == 'Все цеха':
                if name_mashine == 'Null' and number == 'Null' and workgroup == 'Null':
                    mashinslist = MashinsList.objects.all().order_by(sort)
                    data = {
                        'MashinsList': mashinslist,
                        'number': number,
                        'workgroup': workgroup,
                        'ceh': ceh,
                        'name_mashine': name_mashine,
                        'cat': 1,
                        'sort': sort,
                        'page': 'info',
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/data.html", data)
                else:
                    mashinslist = MashinsList.objects.filter(ceh__icontains=workgroup, number__icontains=number,
                                                             name_mashine__icontains=name_mashine).order_by(sort)
                    if workgroup == '' or workgroup == 'Null':
                        ceh = cat_slug
                    else:
                        for mashin in mashinslist:
                            ceh = mashin.ceh
                    data = {
                        'MashinsList': mashinslist,
                        'number': number,
                        'workgroup': workgroup,
                        'ceh': ceh,
                        'name_mashine': name_mashine,
                        'sort': sort,
                        'cat': 1,
                        'page': 'info',
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/data.html", data)
            else:
                if name_mashine == 'Null' and number == 'Null':
                    mashins = MashinsList.objects.filter(ceh=cat_slug).order_by(sort)
                    data = {
                        'cat_slug': cat_slug,
                        'ceh': ceh,
                        'number': number,
                        'name_mashine': name_mashine,
                        'sort': sort,
                        'MashinsList': mashins,
                        'page': 'info',
                    }
                    return render(request, "plant/data.html", data)
                else:
                    mashins = MashinsList.objects.filter(ceh=cat_slug, number__icontains=number,
                                                         name_mashine__icontains=name_mashine).order_by(sort)
                    data = {
                        'cat_slug': cat_slug,
                        'ceh': ceh,
                        'number': number,
                        'name_mashine': name_mashine,
                        'sort': sort,
                        'MashinsList': mashins,
                        'page': 'info',
                    }
                    return render(request, "plant/data.html", data)


@login_required()
def problems(request):
    if request.user.username:
        name = request.user.username
        name_mashine = request.POST.get("name_mashine", 'Null')
        number = request.POST.get("number", 'Null')
        workgroup = request.POST.get("workgroup", 'Null')
        parts = request.POST.get("parts", 'Null')
        num_date = request.POST.get("num_date", '0')
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
            if str(slug.ceh) == 'Все цеха':
                cat = 1
            else:
                cat = 0
            if cat_slug == 'Все цеха':
                if name_mashine == 'Null' and number == 'Null' and workgroup == 'Null' and parts == 'Null' and \
                        num_date == '0':
                    problems = Problems.objects.all().order_by('-start_date')
                    data = {
                        'Problems': problems,
                        'cat': cat,
                        'page': 'problems',
                        'cat_slug': cat_slug,
                        'number': number,
                        'name_mashine': name_mashine,
                        'workgroup': workgroup,
                        'parts': parts,
                        'num_date': num_date,
                    }
                    return render(request, "plant/problems.html", data)
                else:
                    problems = Problems.objects.filter(ceh__icontains=workgroup, number__icontains=number,
                                                       name_mashine__icontains=name_mashine,
                                                       spare_parts__icontains=parts,
                                                       start_date__icontains=num_date).order_by('-start_date')
                    if workgroup != '':
                        for problem in problems:
                            cat_slug = problem.ceh
                    else:
                        workgroup = 'Null'
                    if not number:
                        number = 'Null'
                    if not num_date:
                        num_date = '0'
                    if not name_mashine:
                        name_mashine = 'Null'
                    if not parts:
                        parts = 'Null'
                    data = {
                        'Problems': problems,
                        'cat': cat,
                        'page': 'problems',
                        'cat_slug': cat_slug,
                        'number': number,
                        'name_mashine': name_mashine,
                        'workgroup': workgroup,
                        'parts': parts,
                        'num_date': num_date,
                    }
                    return render(request, "plant/problems.html", data)
            else:
                if name_mashine == 'Null' and number == 'Null' and parts == 'Null':
                    problems = Problems.objects.filter(ceh=cat_slug)
                    data = {
                        'cat_slug': cat_slug,
                        'cat': cat,
                        'Problems': problems,
                        'page': 'problems',
                        'number': number,
                        'name_mashine': name_mashine,
                        'parts': parts,
                    }
                    return render(request, "plant/problems.html", data)
                else:
                    problems = Problems.objects.filter(ceh=cat_slug, number__icontains=number,
                                                       spare_parts__icontains=parts,
                                                       name_mashine__icontains=name_mashine)
                    if not number:
                        number = 'Null'
                    if not name_mashine:
                        name_mashine = 'Null'
                    if not parts:
                        parts = 'Null'
                    data = {
                        'cat_slug': cat_slug,
                        'cat': cat,
                        'Problems': problems,
                        'page': 'problems',
                        'number': number,
                        'name_mashine': name_mashine,
                        'parts': parts,
                    }
                    return render(request, "plant/problems.html", data)


@login_required()
def dto(request):
    now = date.today()
    if request.user.username:
        name = request.user.username
        name_mashine = request.POST.get("name_mashine", 'Null')
        number = request.POST.get("number", 'Null')
        workgroup = request.POST.get("workgroup", 'Null')
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
            if cat_slug == 'Все цеха':
                if name_mashine == 'Null' and number == 'Null' and workgroup == 'Null':
                    dto = DTO.objects.all().order_by('-start_date')
                    data = {
                        'DTO': dto,
                        'cat': 1,
                        'number': number,
                        'name_mashine': name_mashine,
                        'workgroup': workgroup,
                        'page': 'dto',
                        'now': now,
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/dto.html", data)
                else:
                    dto = DTO.objects.filter(ceh__icontains=workgroup, number__icontains=number,
                                             name_mashine__icontains=name_mashine).order_by('-start_date')
                    if workgroup != '':
                        for toir in dto:
                            cat_slug = toir.ceh
                    else:
                        workgroup = 'Null'
                    if not number:
                        number = 'Null'
                    if not name_mashine:
                        name_mashine = 'Null'
                    data = {
                        'DTO': dto,
                        'cat': 1,
                        'number': number,
                        'name_mashine': name_mashine,
                        'workgroup': workgroup,
                        'page': 'dto',
                        'now': now,
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/dto.html", data)
            else:
                if name_mashine == 'Null' and number == 'Null':
                    dto = DTO.objects.filter(ceh=cat_slug).order_by('-start_date')
                    data = {
                        'cat_slug': cat_slug,
                        'DTO': dto,
                        'page': 'dto',
                        'number': number,
                        'name_mashine': name_mashine,
                        'now': now,
                    }
                    return render(request, "plant/dto.html", data)
                else:
                    dto = DTO.objects.filter(ceh=cat_slug, number__icontains=number,
                                             name_mashine__icontains=name_mashine).order_by('-start_date')
                    if not number:
                        number = 'Null'
                    if not name_mashine:
                        name_mashine = 'Null'
                    data = {
                        'cat_slug': cat_slug,
                        'DTO': dto,
                        'page': 'dto',
                        'number': number,
                        'name_mashine': name_mashine,
                        'now': now,
                    }
                    return render(request, "plant/dto.html", data)


@login_required()
def ppr(request):
    now = date.today()
    if request.user.username:
        name = request.user.username
        workgroup = request.POST.get("workgroup", 'Null')
        year = request.POST.get("year", now.year)
        slugs = UserGroup.objects.filter(user=name)
        lst = []
        ppr_dict = {}
        for slug in slugs:
            cat_slug = str(slug.ceh)
            if cat_slug == 'Все цеха':
                if workgroup == 'Null' and year == now.year:
                    mashinslist = MashinsList.objects.all().order_by('number')
                    for mashin in mashinslist:
                        while mashin.register_date.year < year:
                            mashin.register_date = mashin.register_date+relativedelta(months=mashin.to)
                        date_last_year = mashin.register_date - relativedelta(months=mashin.to)
                        while mashin.register_date.year == year:
                            lst.append(mashin.register_date.month)
                            mashin.register_date = mashin.register_date + relativedelta(months=mashin.to)
                        ppr_dict[mashin.number] = lst
                        lst = []
                        mashin.register_date = date_last_year
                    data = {
                        'MashinsList': mashinslist,
                        'cat': 1,
                        'page': 'ppr',
                        'year': year,
                        'ppr_dict': ppr_dict,
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/ppr.html", data)
                else:
                    mashinslist = MashinsList.objects.filter(ceh__icontains=workgroup).order_by('number')
                    if workgroup != '':
                        for mashin in mashinslist:
                            cat_slug = mashin.ceh
                    for mashin in mashinslist:
                        while mashin.register_date.year < int(year):
                            mashin.register_date = mashin.register_date+relativedelta(months=mashin.to)
                        date_last_year = mashin.register_date - relativedelta(months=mashin.to)
                        while mashin.register_date.year == int(year):
                            lst.append(mashin.register_date.month)
                            mashin.register_date = mashin.register_date + relativedelta(months=mashin.to)
                        ppr_dict[mashin.number] = lst
                        lst = []
                        mashin.register_date = date_last_year
                    data = {
                        'MashinsList': mashinslist,
                        'cat': 1,
                        'page': 'ppr',
                        'year': year,
                        'ppr_dict': ppr_dict,
                        'cat_slug': cat_slug,
                    }
                    return render(request, "plant/ppr.html", data)
            else:
                mashins = MashinsList.objects.filter(ceh=cat_slug).order_by('number')
                for mashin in mashins:
                    while mashin.register_date.year < int(year):
                        mashin.register_date = mashin.register_date + relativedelta(months=mashin.to)
                    date_last_year = mashin.register_date - relativedelta(months=mashin.to)
                    while mashin.register_date.year == int(year):
                        lst.append(mashin.register_date.month)
                        mashin.register_date = mashin.register_date + relativedelta(months=mashin.to)
                    ppr_dict[mashin.number] = lst
                    lst = []
                    mashin.register_date = date_last_year
                data = {
                    'cat_slug': cat_slug,
                    'MashinsList': mashins,
                    'page': 'ppr',
                    'ppr_dict': ppr_dict,
                    'year': year,
                }
                return render(request, "plant/ppr.html", data)


@login_required()
def add_data(request):
    if request.method == 'POST':
        form = MashinsListForm(request.POST)
        name = request.user.username
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.ceh = cat_slug
            expense.save()
            # MashinsList.objects.create(**form.cleaned_data)
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
        name = request.user.username
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
        form = DTOForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            mashins = MashinsList.objects.filter(number=expense.number)
            for mashin in mashins:
                expense.name_mashine = mashin.name_mashine
                expense.ceh = mashin.ceh
            expense.save()
            # DTO.objects.create(**form.cleaned_data)
            return redirect('dto')
    else:
        form = DTOForm()
    context = {
        'form': form,
        'title': 'Добавление карты ДТО'
    }
    return render(request, 'plant/add_dto.html', context)


def work(request):
    number = request.POST.get("number", 'Пустой')
    languages = request.POST.getlist("languages")

    # sup_id = 13
    #
    # wsb_seed = 1242649174
    # wsb_storeid = 589839807
    # wsb_order_num = sup_id
    # wsb_test = 1
    # wsb_currency_id = "BYN"
    # wsb_total = 10
    # SecretKey = "12345678901234567890"
    # name = 'Сапборд'
    # reserved_quantity = 1
    # price = total_price = 10
    # customer_name = 'VladLen'
    # email = 'gallvov@tut.by'
    #
    # my_str = str(wsb_seed) + str(wsb_storeid) + str(wsb_order_num) + str(wsb_test) + str(wsb_currency_id) + str(
    #     int(wsb_total)) + str(SecretKey)
    # wsb_signature = hashlib.sha1(my_str.encode('utf-8')).hexdigest()
    #
    # if number == '1':
    #     url = 'https://securesandbox.webpay.by/api/v1/payment'
    #     data = {
    #
    #         # "wsb_storeid": "589839807",
    #         # "wsb_order_num": ids,
    #         # "wsb_currency_id": "BYN",
    #         # "wsb_version": 2,
    #         # "wsb_seed": "1242649174",
    #         # "wsb_test": 1,
    #         # "wsb_invoice_item_name": ["Товар 1"],
    #         # "wsb_invoice_item_quantity": [1],
    #         # "wsb_invoice_item_price": [10],
    #         # "wsb_total": 10,
    #         # "wsb_signature": hex_dig,
    #         # "wsb_3ds_payment_option": "force_3ds",
    #         # "wsb_store": "Название Вашего магазина",
    #         # "wsb_language_id": "russian",
    #         # "wsb_redirect": 1,
    #         # "wsb_return_format": "json",
    #         # "wsb_return_url": f"http://192.168.9.143/good/{ids}",
    #         # "wsb_cancel_return_url": "http://yoursiteurl.com/cancel.php",
    #         # "wsb_notify_url": "http://yoursiteurl.com/notify.php",
    #         # "wsb_customer_name": "Иванов Петр Петрович",
    #         # "wsb_customer_address": "Минск ул. Шафарнянская д.11 оф.54",
    #         # "wsb_service_date": "Доставка до 1 января 2022 года",
    #         # "wsb_tax": 0,
    #         # "wsb_shipping_name": "Стоимость доставки",
    #         # "wsb_shipping_price": 0,
    #         # "wsb_discount_name": "Скидка на товар",
    #         # "wsb_discount_price": 0,
    #         # "wsb_order_tag": "Договор №152/12-1 от 12.01.19",
    #         # "wsb_email": "ivanov@test.by",
    #         # "wsb_phone": "375291234567",
    #         # "wsb_order_contract": "Договор №152/12-1 от 12.01.19",
    #         # "wsb_tab": "cardPayment",
    #         # # "wsb_startsesstime": "1603383601",
    #         # # "wsb_startsessdatetime": "2020-10-22T16:20:01+03:00"
    #
    #         "wsb_storeid": "589839807",
    #         "wsb_order_num": sup_id,
    #         "wsb_currency_id": "BYN",
    #         "wsb_version": 2,
    #         "wsb_seed": "1242649174",
    #         "wsb_test": 1,
    #         "wsb_invoice_item_name": [name],
    #         "wsb_invoice_item_quantity": [reserved_quantity],
    #         "wsb_invoice_item_price": [price],
    #         "wsb_total": total_price,
    #         "wsb_signature": wsb_signature,
    #         "wsb_3ds_payment_option": "force_3ds",
    #         "wsb_store": "Boardhouse",
    #         "wsb_language_id": "russian",
    #         "wsb_redirect": 1,
    #         "wsb_return_format": "json",
    #         "wsb_return_url": f'https://boardhouse.by/booking/goodpaymentSup/{sup_id}',
    #         "wsb_cancel_return_url": f'https://boardhouse.by/booking/badpaymentSup/{sup_id}',
    #         # "wsb_notify_url": "http://yoursiteurl.com/notify.php",
    #         "wsb_customer_name": customer_name,
    #         # "wsb_customer_address": "Минск ул. Шафарнянская д.11 оф.54",
    #         # "wsb_service_date": "Доставка до 1 января 2025 года",
    #         # "wsb_tax": 0,
    #         # "wsb_shipping_name": "Стоимость доставки",
    #         # "wsb_shipping_price": 0,
    #         # "wsb_discount_name": "Скидка на товар",
    #         # "wsb_discount_price": 0,
    #         # "wsb_order_tag": "Договор №152/12-1 от 12.01.19",
    #         "wsb_email": email,
    #         # "wsb_phone": "375291234567",
    #         # "wsb_order_contract": "Договор №152/12-1 от 12.01.19",
    #         "wsb_tab": "cardPayment",
    #         # "wsb_startsesstime": "1603383601",
    #         # "wsb_startsessdatetime": "2020-10-22T16:20:01+03:00"
    #     }
    #     response = requests.post(url, json=data)
    #     res = response.text
    #     res = json.loads(res)
    #     print(res)
    #     redirect_url = res['data']['redirectUrl']
    #     return redirect(redirect_url)
    # else:
    #     data = {
    #         'number': number,
    #     }
    #     return render(request, 'plant/work.html', data)
    print(languages)
    print(type(languages))
    if number == '':
        number = 'Пустой'
    if languages == False:
        languages = 'Пустой'
    data = {
        'number': number,
        'languages': languages,
    }
    print(','.join(languages))
    return render(request, 'plant/work.html', data)


def good(request, ids):
    data = {
        'ids': ids,
    }
    return render(request, 'plant/good.html', data)


def news(request):
    data = {
        'page': 'news',
    }
    return render(request, 'plant/news.html', data)


def nogood(request):
    return render(request, 'plant/nogood.html')


class UpdateDTOUser(UpdateView):
    model = DTO
    fields = ['number', 'name_mashine', 'ceh', 'start_date', 'finish_date', 'next_to', 'document',
              'responsible', 'comment', 'status']
    template_name = 'plant/add_dto.html'
    success_url = reverse_lazy('dto')
    title_page = 'Редактирование карты ДТО'
    extra_context = {
        'title': 'Редактирование карты ДТО',
    }


class UpdateDTO(UpdateView):
    model = DTO
    fields = ['number', 'name_mashine', 'ceh', 'start_date', 'finish_date', 'document', 'responsible', 'status']
    template_name = 'plant/add_dto.html'
    success_url = reverse_lazy('dto')
    title_page = 'Редактирование карты ДТО'
    extra_context = {
        'title': 'Редактирование карты ДТО',
    }


class UpdateMashinsList(UpdateView):
    model = MashinsList
    form_class = MashinsListForm
    # fields = ['number', 'name_mashine', 'ceh', 'manufacturer', 'number_plant', 'build_date', 'register_date', 'form',
    #           'to', 'photo', 'nameplate', 'status', 'characteristics']
    template_name = 'plant/add_data.html'
    success_url = reverse_lazy('data')
    title_page = 'Редактирование характеристик оборудования'
    extra_context = {
        'title': 'Редактирование характеристик оборудования',
    }


class UpdateProblemsUser(UpdateView):
    model = Problems
    form_class = ProblemsFormMaster
    # fields = ['number', 'name_mashine', 'ceh', 'start_date', 'description', 'comp_work', 'spare_parts', 'status',
    #           'finish_date', 'responsible', 'comment']
    template_name = 'plant/add_problems.html'
    success_url = reverse_lazy('problems')
    title_page = 'Редактирование неполадок оборудования'
    extra_context = {
        'title': 'Редактирование неполадок оборудования',
    }


class UpdateProblems(UpdateView):
    model = Problems
    form_class = ProblemsFormUser
    # fields = ['number', 'name_mashine', 'ceh', 'start_date', 'description', 'comp_work', 'spare_parts', 'status',
    #           'finish_date', 'responsible']
    template_name = 'plant/add_problems.html'
    success_url = reverse_lazy('problems')
    title_page = 'Редактирование неполадок оборудования'
    extra_context = {
        'title': 'Редактирование неполадок оборудования',
    }


@login_required()
def add_problems(request):
    if request.user.username:
        name = request.user.username
        slugs = UserGroup.objects.filter(user=name)
        for slug in slugs:
            cat_slug = str(slug.ceh)
            if cat_slug == 'Все цеха':
                if request.method == 'POST':
                    form = ProblemsFormMaster(request.POST)
                    if form.is_valid():
                        expense = form.save(commit=False)
                        mashins = MashinsList.objects.filter(number=expense.number)
                        for mashin in mashins:
                            expense.name_mashine = mashin.name_mashine
                        expense.ceh = cat_slug
                        expense.save()
                        # Problems.objects.create(**form.cleaned_data)
                        return redirect('problems')
                else:
                    form = ProblemsFormMaster()
                context = {
                    'form': form,
                    'title': 'Добавление неполадки'
                }
                return render(request, 'plant/add_problems.html', context)
            else:
                if request.method == 'POST':
                    form = ProblemsFormUser(request.POST)
                    if form.is_valid():
                        expense = form.save(commit=False)
                        mashins = MashinsList.objects.filter(number=expense.number)
                        for mashin in mashins:
                            expense.name_mashine = mashin.name_mashine
                        expense.ceh = cat_slug
                        expense.save()
                        # Problems.objects.create(**form.cleaned_data)
                        return redirect('problems')
                else:
                    form = ProblemsFormUser()
                context = {
                    'form': form,
                    'title': 'Добавление неполадки'
                }
                return render(request, 'plant/add_problems.html', context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

