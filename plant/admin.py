from django.contrib import admin

from .models import Ceh, MashinsList, Problems, DTO, UserGroup


@admin.register(Ceh)
class CehAdmin(admin.ModelAdmin):
    list_display = ('ceh',)


@admin.register(MashinsList)
class MashinsListAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_mashine', 'ceh', 'pub_date')


@admin.register(Problems)
class ProblemsAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_mashine', 'start_date', 'description', 'pub_date')


@admin.register(DTO)
class DTOAdmin(admin.ModelAdmin):
    list_display = ('number', 'name_mashine', 'start_date', 'pub_date')


@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'ceh')
