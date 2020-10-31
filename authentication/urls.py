from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('add_users/', views.add_users, name='add_users'),
    path('view_all_users/', views.view_all_users, name='view_all_users'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('disable_user/', views.disable_user, name='disable_user'),
    path('enable_user/', views.enable_user, name='enable_user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('redirect_login/', views.redirect_login, name='redirect_login'),
    path('logout/', views.logout, name='logout')
]
