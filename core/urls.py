from django.contrib import admin
from django.urls import path, include
from .views import home,salvar,edit,delete,update,incluir,pagInicial,subir,descer

urlpatterns = [
    path('', home),
    path('incluir/', incluir, name="incluir"),
    path('pagInicial/', pagInicial, name="pagInicial"),
    path('salvar/', salvar, name="salvar"),
    path('edit/<int:id>', edit, name="edit"),
    path('update/<int:id>', update, name="update"),
    path('delete/<int:id>', delete, name="delete"),
    path('subir/<int:ordemApresentacao>/', subir, name="subir"),
    path('descer/<int:ordemApresentacao>/', descer, name="descer"),
]