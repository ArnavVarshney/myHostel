from django.urls import path

from snacks import views

urlpatterns = [
    path('view_all_previous_snacks/', views.view_all_previous_snacks, name='view_all_previous_snacks'),
    path('view_snacks_info/', views.view_snacks_info, name='view_snacks_info'),
    path('create_snacks/', views.create_snacks, name='create_snacks'),
    path('view_pending_snacks/', views.view_pending_snacks, name='view_pending_snacks'),
    path('upload_bills/', views.upload_bills, name='upload_bills')
]
