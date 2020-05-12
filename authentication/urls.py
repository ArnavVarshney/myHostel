from django.urls import path

from authentication import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout, name='logout')
]
