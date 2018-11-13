from django.contrib import admin
from app.models import ProjectxUser, Message, Config


class projectx_userAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone')


class messageAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'message', 'created_date', 'chat')


class configAdmin(admin.ModelAdmin):
    list_display = ('chat_max_number',)


admin.site.register(ProjectxUser, projectx_userAdmin)
admin.site.register(Message, messageAdmin)
admin.site.register(Config, configAdmin)
