from django.contrib import admin
from chat.models import Messages

class MessagesAdmin(admin.ModelAdmin):
    list_display = ['user', 'reciepient','body','is_read']
admin.site.register(Messages,MessagesAdmin)