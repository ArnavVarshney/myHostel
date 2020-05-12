from django.contrib import admin
from django.urls import path, include

from myHostel import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authentication/', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls)
]
