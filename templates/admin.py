from django.contrib import admin
from .models import MessageTemplate, SubjectTemplate


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'industry', 'used', 'replied', 'succeeded', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['content', 'industry']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SubjectTemplate)
class SubjectTemplateAdmin(admin.ModelAdmin):
    list_display = ['content', 'used', 'replied', 'succeeded', 'created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']

