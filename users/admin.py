from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at', 'updated_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']

