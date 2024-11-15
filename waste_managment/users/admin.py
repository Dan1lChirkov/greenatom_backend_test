from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'organizations')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser', 'groups',
            'user_permissions'
        )}),
        (_('Organizations'), {'fields': ('organizations',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'password1',
                'password2', 'organizations', 'is_staff', 'is_active'
            ),
        }),
    )

    readonly_fields = ('last_login', 'date_joined')

    ordering = ('id',)

    filter_horizontal = ('organizations', 'groups', 'user_permissions')
