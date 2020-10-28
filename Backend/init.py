import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vision_space.settings")
django.setup()

from board.models import Type

for name in ("text", "image", "embed_video", "link"):
    new_type = Type()
    new_type.name = name
    new_type.save()

print("DATA INITIALIZE COMPLETE!")