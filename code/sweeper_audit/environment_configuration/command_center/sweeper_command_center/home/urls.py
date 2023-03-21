from django.urls import path
from django.urls import re_path as url
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('index_normal', views.index_normal, name='index_normal'),
    path('charts', views.charts, name='charts'),
    path('charts_normal', views.charts_normal, name='charts_normal'),
    path('tables', views.tables, name='tables'),
    path('tables_normal', views.tables_normal, name='tables_normal'),
    path('', views.login, name='login'),
    url(r'^drop_info_index/', views.drop_info_index),
    url(r'^drop_info_tables/', views.drop_info_tables),
    url(r'^generate_new_detail_info/', views.generate_new_detail_info),
    url(r'^generate_report/', views.generate_report),
    url(r'^drop_report/', views.drop_report),
]