from django.contrib import admin
from app.models import projectx_user


class projectx_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone')


admin.site.register(projectx_user, projectx_userAdmin)
