from django.db import models
from core.models import BaseModel
from apps.polls.models import Poll
from apps.choices.models import Choice
from django.contrib.auth.models import User

class Vote(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)


    class Meta:
        unique_together = ('user', 'poll')
