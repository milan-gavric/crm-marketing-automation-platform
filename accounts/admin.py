from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'first_name', 'last_name', 'main_email', 'created_at']
    search_fields = ['name', 'main_email']
    readonly_fields = ['created_at', 'updated_at']

