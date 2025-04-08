from django.db import models
from core.models import BaseModel

class Poll(BaseModel):
    question = models.CharField(max_length=255)
