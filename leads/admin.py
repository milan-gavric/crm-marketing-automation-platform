from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['Email', 'status', 'first_name', 'last_name', 'company', 'assigned_to', 'created_at']
    list_filter = ['status', 'assigned_to', 'created_at']
    search_fields = ['Email', 'first_name', 'last_name', 'company']
    readonly_fields = ['created_at', 'updated_at']

