from django.db import models
from django.utils import timezone

import datetime

class Question(models.Model):
    # id = models.IntegerField(primary_key=True) # Django does this automatically
    text = models.CharField(max_length=500, null=False)
    pub_date = models.DateTimeField("date published", null=False)
    
    def __str__(self) -> str:
        return self.text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.id)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_choices")
    text = models.CharField(max_length=500, null=False)
    votes = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return self.text