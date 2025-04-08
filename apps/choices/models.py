from django.db import models
from core.models import BaseModel
from apps.polls.models import Poll

class Choice(BaseModel):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
