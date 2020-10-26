from django.db import models
from django.conf import settings

# Create your models here.
class Board(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)  # 보드를 생성/관리하는 메인 관리자
    name = models.CharField(max_length=50)

class Tab(models.Model):
    board_pk = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class Type(models.Model):
    name = models.CharField(max_length=20)

class Note(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    tab_pk = models.ForeignKey(Tab, on_delete=models.CASCADE)
    type_pk = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    content = models.TextField()
    lock = models.BooleanField()

class History(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    tab_pk = models.ForeignKey(Tab, on_delete=models.CASCADE)
    note_pk = models.ForeignKey(Note, on_delete=models.DO_NOTHING)
    type_pk = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
