from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'poll', 'choice', 'created_at')
    search_fields = ('user__username', 'poll__question', 'choice__text')
    list_filter = ('poll', 'choice', 'created_at')
    ordering = ('-created_at',)
