from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_view
from . import views
from .views import LoginUser, UpdateDTO, UpdateMashinsList, UpdateProblems, UpdateProblemsUser, UpdateDTOUser

urlpatterns = [
    path('data/', views.data, name='data'),
    # path('seach_data/', views.seach_data, name='seach_data'),
    # path('data/<slug:cat_slug>/', views.data_slug, name='data_ceh'),
    path('problems/', views.problems, name='problems'),
    path('dto/', views.dto, name='dto'),
    path('ppr/', views.ppr, name='ppr'),
    path('work/', views.work, name='work'),
    path('good/<int:ids>', views.good, name='good'),
    path('nogood/', views.nogood, name='nogood'),
    path('news/', views.news, name='news'),
    # path('problems/<slug:cat_slug>/', views.problems_slug),
    # path('dto/<slug:cat_slug>/', views.dto_slug),
    path('add_dto/', views.add_dto, name='add_dto'),
    path('add_problems/', views.add_problems, name='add_problems'),
    path('add_data/', views.add_data, name='add_data'),
    path('update/<int:pk>/dtouser/', UpdateDTOUser.as_view(), name='edit_dto_user'),
    path('update/<int:pk>/dto/', UpdateDTO.as_view(), name='edit_dto'),
    path('update/<int:pk>/data/', UpdateMashinsList.as_view(), name='edit_data'),
    path('update/<int:pk>/problemsuser/', UpdateProblemsUser.as_view(), name='edit_problems_user'),
    path('update/<int:pk>/problems/', UpdateProblems.as_view(), name='edit_problems'),
    path('', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
