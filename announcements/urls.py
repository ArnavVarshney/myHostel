from django.urls import path

from announcements import views

urlpatterns = [
    path('create_announcement', views.create_announcement, name='create_announcement'),
]
