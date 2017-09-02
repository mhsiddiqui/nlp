# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models

# Create your models here.
from django.dispatch import receiver


def upload_file(instance, filename):
    timestamp = re.sub('[^A-Za-z0-9]+', '', str(instance.time))
    return 'voice/{ip}/{timestamp}/{filename}'.format(**{
        "ip": instance.ip, "timestamp": timestamp, "filename": "voice.wav"
    })


class GeneratedVoice(models.Model):
    file = models.FileField(upload_to=upload_file)
    text = models.CharField(default='', max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(default='', max_length=100)


@receiver(models.signals.pre_delete, sender=GeneratedVoice)
def remove_chat_media_from_s3(sender, instance, **kwargs):
    instance.file.delete(save=False)
