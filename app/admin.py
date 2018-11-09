from django.contrib import admin
from app.models import ProjectxUser, Message


class projectx_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone')


class messageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'message', 'created_date')


admin.site.register(ProjectxUser, projectx_userAdmin)
admin.site.register(Message, messageAdmin)
