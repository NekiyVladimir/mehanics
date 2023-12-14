from django.db import models
from django.urls import reverse


STATUS_CHOICES = [
    ('OK', 'Все верно'),
    ('NO', 'Требует доработок')
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
    group = models.CharField(max_length=10, verbose_name='Группа')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user


class MashinsList(models.Model):
    number = models.CharField(max_length=10, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования')
    ceh = models.ForeignKey('Ceh', on_delete=models.CASCADE, null=True, blank=True)
    # ceh = models.CharField(max_length=10, verbose_name='Цех', null=True)
    register_date = models.CharField(max_length=100, verbose_name='Дата ввода в эксплуатацию')
    manufacturer = models.CharField(max_length=100, verbose_name='Изготовитель', blank=True, null=True)
    number_plant = models.CharField(max_length=100, verbose_name='Заводской номер', blank=True, null=True)
    build_date = models.IntegerField(verbose_name='Дата изготовления', blank=True, null=True)
    characteristics = models.TextField(verbose_name='Характеристики оборудования')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус")
    photo = models.ImageField(upload_to='photo_mashins', verbose_name='Фото оборудования',  blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Ооборудование'
        verbose_name_plural = 'Характеристики оборудования'

    def __str__(self):
        return self.name_mashine


class Problems(models.Model):
    number = models.CharField(max_length=10, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования')
    ceh = models.ForeignKey('Ceh', on_delete=models.CASCADE, null=True, blank=True)
    # ceh = models.CharField(max_length=10, verbose_name='Цех', null=True)
    start_date = models.DateField(verbose_name='Дата выявления неполадки')
    description = models.TextField(verbose_name='Описание неполадки')
    photo_problem = models.ImageField(upload_to='photo_problems', verbose_name='Фото неполадки',  blank=True)
    comp_work = models.TextField(verbose_name='Выполненые работы', blank=True)
    spare_parts = models.CharField(max_length=300, verbose_name='Запчасти', blank=True)
    status = models.CharField(max_length=50, verbose_name='Статус', blank=True)
    finish_date = models.DateField(verbose_name='Дата устранения неполадки', blank=True)
    responsible = models.CharField(max_length=50, verbose_name='Отвественный', blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус")
    comment = models.TextField(verbose_name='Комментарий',  blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Неполадки'
        verbose_name_plural = 'Неполадки'

    def __str__(self):
        return self.name_mashine


class DTO(models.Model):
    number = models.CharField(max_length=30, verbose_name='Инв.№')
    name_mashine = models.CharField(max_length=300, verbose_name='Наименование оборудования')
    ceh = models.ForeignKey('Ceh', on_delete=models.CASCADE, null=True, blank=True)
    # ceh = models.CharField(max_length=10, verbose_name='Цех', null=True)
    start_date = models.DateField(verbose_name='Дата проведения ДТО')
    document = models.FileField(upload_to='scan_card', verbose_name='Скан документа', blank=True, null=True)
    responsible = models.CharField(max_length=50, verbose_name='Ответственный')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, verbose_name="Статус")
    comment = models.TextField(verbose_name='Комментарий',  blank=True)
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации', null=True)

    class Meta:
        verbose_name = 'Карты ДТО'
        verbose_name_plural = 'Карты ДТО'

    def __str__(self):
        return self.name_mashine






