from django.urls import path
from . import views

app_name = 'intent_marker'
urlpatterns = [
    path('', views.index, name='index'),
    path('dialog/save_data', views.save_data, name='save_data'),
    path('dialog/<str:user>', views.dialog, name='dialog'),
    path('stat/', views.total_stat, name='total_stat'),
    path('pie/', views.topic_pie, name='topic_pie'),
    # path('stat/<str:user>', views.user_stat, name='user_stat'),
    # path('stat/date/<str:dte>', views.date_stat, name='date_stat'),
    path('report/', views.marked_results_report_index, name='report_index'),
    path('report/total', views.marked_results_total_report, name='report_total'),
    path('report/detail/<str:chat_dte>', views.marked_results_report_by_date, name='report_by_date'),
    path('report/save/<str:chat_dte>', views.marked_results_save_report, name='save_report'),
]
