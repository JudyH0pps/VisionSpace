import os
from uuid import uuid4
from datetime import datetime
from django.db import models

def get_file_path(instance, filename):
    # ext = filename.split('.')[-1]
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    uuid_name = "{}".format(uuid4().hex)
    return '/'.join(['files/', ymd_path, uuid_name])

class File(models.Model):
    file = models.FileField(upload_to=get_file_path, blank=False, null=True)
    filename = models.CharField(max_length=64, null=True)
    hex_name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.file.name
