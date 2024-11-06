# models.py
from typing import Iterable
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
 
class Keyword(models.Model):
    keyword = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, default='pending')  # Add this line

    def __str__(self):
        return self.keyword

class KeywordResult(models.Model):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    url = models.URLField()
    position = models.IntegerField()
    page_number = models.IntegerField()

    def __str__(self):
        return f"{self.keyword} - {self.url}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


@receiver(post_save, sender=KeywordResult)
def notification(sender, instance, created, *args, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_group",
        {
            "type": "chat_notification",
            "keyword": instance.keyword.keyword,
            "scheduled_time": str(instance.keyword.scheduled_time),
            "url" : instance.url,
            "position" : instance.position,
            "page_number" : instance.page_number,
            
        },
    )
