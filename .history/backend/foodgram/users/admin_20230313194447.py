from django.contrib import admin

from .models import User, Follow

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'email',
        'username',
    )
    search_fields = (
        'email',
        'username',
    )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    list_filter = (
        'user',
        'author',
    )
    search_fields = ('author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)