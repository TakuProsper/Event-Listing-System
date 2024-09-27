from django.contrib import admin
from .models import CustomUser,Profile

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


class ProfileAdmin(admin.ModelAdmin):
    list_editable = ['verified']
    list_display = ['user', 'full_name' ,'verified']

admin.site.register(CustomUser, UserAdmin)
admin.site.register( Profile,ProfileAdmin)