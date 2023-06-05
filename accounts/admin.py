from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

from django.utils.html import format_html

#User Accounts admin
class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active',)
    list_display_links = ('email','first_name','last_name',)
    readonly_fields = ('last_login','date_joined',)
    ordering = ('date_joined',)

    #We have to put these beacause we are using abstractBaseUser
    filter_horizontal = ()
    list_filter = ()
    fieldsets = () #put the password on read only

admin.site.register(Account,AccountAdmin)

#User profile admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'address_line','created_at','modified_at')
    list_display_links = ('user', 'city', 'address_line',)

admin.site.register(UserProfile,UserProfileAdmin)
