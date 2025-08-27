from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('agendar-consulta/', views.agendar_consulta_view, name='agendar_consulta')
]