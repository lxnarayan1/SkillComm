from django.contrib import admin
from .models import ExchangeRequest

@admin.register(ExchangeRequest)
class ExchangeRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'skill_offered', 'skill_requested', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'skill_offered__name', 'skill_requested__name']
    readonly_fields = ['created_at', 'updated_at']
