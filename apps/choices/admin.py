from django.contrib import admin
from .models import Choice

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'poll', 'text', 'created_at', 'updated_at')
    search_fields = ('text', 'poll__question')
    list_filter = ('poll', 'created_at', 'updated_at')
    ordering = ('-created_at',)
