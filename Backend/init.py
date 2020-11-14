import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vision_space.settings")
django.setup()

from board.models import Type

for name in ("text", "file", "embed_video", "link", "user_video"):
    new_type = Type()
    new_type.name = name
    new_type.save()

print("DATA INITIALIZE COMPLETE!")
