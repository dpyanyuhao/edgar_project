from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph/', views.graph, name='graph'),
    path('test_graph/', views.test_alt, name='test'),
    path('dropdown/', views.dropdown, name='dropdown'),
]