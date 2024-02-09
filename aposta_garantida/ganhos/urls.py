from django.urls import path
from . import views
from .views import CampoUpdate, CampoList, CampoCreate, CampoDelete, LucrosDayListView, black_list

urlpatterns = [
    path('', CampoList.as_view(), name='listar-campo'),
    path('home', CampoList.as_view(), name='listar-campo'),
    path('deleta/member/<int:pk>', CampoDelete.as_view(), name='deleta-campo'),
    path('editar/member/<int:pk>', CampoUpdate.as_view(), name='editar-status'),
    path('cadastrar/campo', CampoCreate.as_view(), name='cadastrar-campo'),
    path('saldo/', views.saldo, name='saldo'),
    path('lucros_day/', LucrosDayListView.as_view(), name='lucros_day'),
    path('black_list/', views.black_list, name='black_list'),
    path('dropbox/', views.dropbox, name='dropbox'),
]
