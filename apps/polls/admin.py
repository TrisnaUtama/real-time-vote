from django.contrib import admin
from .models import Poll

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'created_at', 'updated_at')
    search_fields = ('question',)
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
