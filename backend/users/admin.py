from django.contrib import admin

from .models import Follow
from .models import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    search_fields = (
        'email',
        'username',
        'first_name',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    search_fields = (
        'user',
    )
