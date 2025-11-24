from django.contrib import admin
from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'account', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at', 'updated_at']

