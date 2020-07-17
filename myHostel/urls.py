from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from myHostel import views, settings

urlpatterns = [
    path('', views.index, name='index'),
    path('authentication/', include('authentication.urls')),
    path('announcements/', include('announcements.urls')),
    path('weekly_report/', include('weekly_report.urls')),
    path('permissions/', include('permissions.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('snacks/', include('snacks.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
