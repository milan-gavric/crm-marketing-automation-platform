"""
URL configuration for CRM Marketing Automation Platform.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'ok', 'message': 'Server is running'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/account/', include('accounts.urls')),
    path('api/lead/', include('leads.urls')),
    path('api/email/', include('emails.urls')),
    path('api/template/', include('templates.urls')),
    path('health', health_check, name='health'),
]

