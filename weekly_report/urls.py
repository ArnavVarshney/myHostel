from django.urls import path

from weekly_report import views

urlpatterns = [
    path('fill_report/', views.fill_report, name='fill_report'),
    path('create_report/', views.create_report, name='create_report'),
    path('view_pending_reports/', views.view_pending_reports, name='view_pending_reports'),
    path('view_all_previous_reports/', views.view_all_previous_reports, name='view_all_previous_reports'),
    path('view_report_info/', views.view_report_info, name='view_report_info'),
    path('view_previous_reports/', views.view_previous_reports, name='view_previous_reports')
]
