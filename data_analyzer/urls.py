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
    path('application_two/', views.application_two, name='application_two'),
    path('get_time_intervals/', views.get_time_intervals, name='get_time_intervals'),
    path('get_time_intervals_by_cusip/', views.get_time_intervals_by_cusip, name='get_time_intervals_by_cusip'),
    path('get_fund_holdings_plot/', views.get_fund_holdings_plot, name='get_fund_holdings_plot'),
    path('get_dollar_notional_plot/', views.get_dollar_notional_plot, name='get_dollar_notional_plot'),
    path('get_top_holdings_plot/', views.get_top_holdings_plot, name='get_top_holdings_plot'),
    path('get_sector_exposure_plot/', views.get_sector_exposure_plot, name='get_sector_exposure_plot'),
    path('get_position_change_table/', views.get_position_change_table, name='get_position_change_table'),
]