import os, uuid
from django.db import models

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)

class File(models.Model):
    file = models.FileField(upload_to=get_file_path, blank=False, null=False)
    def __str__(self):
        return self.file.name
