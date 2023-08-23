from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph/', views.graph, name='graph'),
    path('test_graph/', views.test_alt, name='test'),
    path('dropdown/', views.dropdown, name='dropdown'),
    path('landing/', views.landing, name='landing'),
    path('get_filtered_positions/', views.get_filtered_positions, name='get_filtered_positions'),
    path('application_one/', views.application_one, name='application_one'),
    path('get_time_intervals/', views.get_time_intervals, name='get_time_intervals'),
    path('get_cik_and_time/', views.get_cik_and_time, name='get_cik_and_time'),
]