from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'password', 'email', 'first_name', 'last_name'
    )
    search_fields = ('username',)
    list_filter = ('username', 'email')