from django.urls import path

from permissions import views

urlpatterns = [
    path('new_request/', views.new_request, name='new_request'),
    path('view_previous_requests/', views.view_previous_requests, name='view_previous_requests'),
    path('view_all_previous_requests/', views.view_all_previous_requests, name='view_all_previous_requests'),
    path('approve_request/', views.approve_request, name='approve_request'),
    path('reject_request/', views.reject_request, name='reject_request'),
    path('withdraw_request/', views.withdraw_request, name='withdraw_request'),
    path('edit_request/', views.edit_request, name='edit_request'),
    path('review_requests/', views.review_requests, name='review_requests')
]
