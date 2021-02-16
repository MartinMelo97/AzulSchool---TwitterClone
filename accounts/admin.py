from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TwitterUser, Follow

class TwitterUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Profile Information', {
            'fields': ('bio', 'date_birth', 'profile_photo', 'cover_photo')
        })
    )


admin.site.register(TwitterUser, TwitterUserAdmin)
admin.site.register(Follow)

# Register your models here.
