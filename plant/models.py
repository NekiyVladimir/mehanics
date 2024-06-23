# import os

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import TextInput, Textarea
from django.urls import reverse
# from django.core.files.storage import FileSystemStorage

# from mehanics import settings


# class ReplacingFileStorage(FileSystemStorage):
#     def get_available_name(self, name, max_length=None):
#         if self.exists(name):
#             os.remove(os.path.join(settings.MEDIA_ROOT, name))
#         return name


STATUS_CHOICES = [
    ('OK', 'Все верно'),
    ('NO', 'Требует доработок'),
]

NEXT_CHOICE = [
    ('Да', 'Да'),
    ('Нет', 'Нет'),
]

WORKGROUP_CHOICE = [
    ('№ 1', '№ 1'),
    ('№ 2', '№ 2'),
    ('№ 3', '№ 3'),
    ('№ 4', '№ 4'),
    ('№ 5', '№ 5'),
    ('№ 6', '№ 6'),
    ('№ 7', '№ 7'),
    ('№ 8', '№ 8'),
    ('№ 9', '№ 9'),
    ('№ 10', '№ 10'),
    ('№ 11', '№ 11'),
    ('№ 21', '№ 21'),
    ('№ 16', '№ 16'),
    ('№ 17', '№ 17'),
    ('№ 18', '№ 18'),
    ('№ 19', '№ 19'),
    ('ЭПЦ', 'ЭПЦ'),
    ('Все цеха', 'Все цеха'),
]


class Ceh(models.Model):
    ceh = models.CharField(max_length=5, verbose_name='Цех')

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'

    def __str__(self):
        return self.ceh

    def get_absolute_url(self):
        return reverse('index_ceh', args=[str(self.ceh)])


class UserGroup(models.Model):
    user = models.CharField(max_length=20, verbose_name='Пользователь')
    ceh = models.CharField(choices=WORKGROUP_CHOICE, max_length=10, verbose_name="Цех", default='Цех № 1')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user


class MashinsList(models.Model):
    number = models.CharField(max_length=10, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования')
    ceh = models.CharField(choices=WORKGROUP_CHOICE, max_length=10, verbose_name="Цех", default='Цех № 1')
    register_date = models.DateField(verbose_name='Дата регистрации')
    to = models.IntegerField(verbose_name='Периодичность ТОиР (месяцев)', default=2)
    manufacturer = models.CharField(max_length=100, verbose_name='Изготовитель', blank=True)
    number_plant = models.CharField(max_length=100, verbose_name='Заводской номер', blank=True)
    build_date = models.CharField(max_length=12, verbose_name='Дата изготовления', default='-', blank=True)
    characteristics = models.TextField(verbose_name='Характеристики оборудования')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус", default='NO')
    photo = models.FileField(upload_to='photo_mashins', verbose_name='Фото оборудования',  blank=True)
    nameplate = models.FileField(upload_to='photo_mashins', verbose_name='Фото таблики оборудования', blank=True,
                                 null=True)
    form = models.FileField(upload_to='form_mashins', verbose_name='Карта ТОиР',  blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Ооборудование'
        verbose_name_plural = 'Характеристики оборудования'
        constraints = (
            models.UniqueConstraint(
                fields=('number',),
                name='person_number_unique'
            ),
        )

    def __str__(self):
        return self.name_mashine


@receiver(pre_save, sender=MashinsList)
def pre_save_photo(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.photo.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


@receiver(pre_save, sender=MashinsList)
def pre_save_form(sender, instance, *args, **kwargs):
    try:
        old_form = instance.__class__.objects.get(id=instance.id).form.path
        try:
            new_form = instance.form.path
        except:
            new_form = None
        if new_form != old_form:
            import os
            if os.path.exists(old_form):
                os.remove(old_form)
    except:
        pass


@receiver(pre_save, sender=MashinsList)
def pre_save_nameplate(sender, instance, *args, **kwargs):
    try:
        old_nameplate = instance.__class__.objects.get(id=instance.id).nameplate.path
        try:
            new_nameplate = instance.nameplate.path
        except:
            new_nameplate = None
        if new_nameplate != old_nameplate:
            import os
            if os.path.exists(old_nameplate):
                os.remove(old_nameplate)
    except:
        pass


class Problems(models.Model):
    number = models.CharField(max_length=10, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования', default='-')
    ceh = models.CharField(choices=WORKGROUP_CHOICE, max_length=10, verbose_name="Цех", default='Цех № 1')
    start_date = models.DateField(verbose_name='Дата выявления неполадки')
    description = models.TextField(verbose_name='Описание неполадки')
    photo_problem = models.ImageField(upload_to='photo_problems', verbose_name='Фото неполадки',  blank=True)
    comp_work = models.TextField(verbose_name='Выполненые работы', blank=True)
    spare_parts = models.CharField(max_length=300, verbose_name='Запчасти', blank=True)
    finish_date = models.DateField(verbose_name='Дата устранения неполадки', blank=True, null=True)
    responsible = models.CharField(max_length=50, verbose_name='Отвественный', blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус", default='NO')
    comment = models.TextField(verbose_name='Комментарий',  blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Неполадки'
        verbose_name_plural = 'Неполадки'

    def __str__(self):
        return self.name_mashine


@receiver(pre_save, sender=Problems)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo_problem.path
        try:
            new_img = instance.photo_problem.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


class DTO(models.Model):
    number = models.CharField(max_length=30, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования', default='-')
    ceh = models.CharField(choices=WORKGROUP_CHOICE, max_length=10, verbose_name="Цех", default='Цех № 1')
    start_date = models.DateField(verbose_name='Дата начала ТОиР')
    finish_date = models.DateField(verbose_name='Дата окончания ТОиР')
    next_date = models.DateField(verbose_name="Предварительная дата ТОиР", blank=True, null=True)
    next_to = models.CharField(choices=NEXT_CHOICE, max_length=10, verbose_name="Принята карта ТОиР", default='Нет')
    document = models.FileField(upload_to='scan_card', verbose_name='Скан документа', blank=True, null=True)
    responsible = models.CharField(max_length=50, verbose_name='Ответственный', default='-')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус", default='NO')
    comment = models.TextField(verbose_name='Комментарий',  blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', null=True)

    class Meta:
        verbose_name = 'Карты ДТО'
        verbose_name_plural = 'Карты ДТО'

    def __str__(self):
        return self.name_mashine


@receiver(pre_save, sender=DTO)
def pre_save_image(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).document.path
        try:
            new_img = instance.document.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass


# class News(models.Model):
#     id_list =
#     name = models.CharField(max_length=300, verbose_name='Название')
#     text_news = models.TextField(verbose_name='Текст')
