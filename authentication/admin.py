from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser, Group

from authentication.models import User

admin.site.register(User)
admin.site.unregister(Group)
admin.site.unregister(DjangoUser)
