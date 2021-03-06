import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=50)
    super_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    user_list = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_boards", through="User_Board")  # 보드를 생성/관리하는 메인 관리자
    max_tab_index = models.IntegerField(default=0)
    session_id = models.CharField(max_length=50, default=uuid.uuid4, unique=True)

class User_Board(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    board_pk = models.ForeignKey(Board, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField()

class Type(models.Model):
    name = models.CharField(max_length=20)

class Tab(models.Model):
    board_pk = models.ForeignKey(Board, on_delete=models.CASCADE)
    tab_index = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    max_note_index = models.IntegerField(default=0)
    max_tm_index = models.IntegerField(default=0)

class Note(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    board_pk = models.ForeignKey(Board, on_delete=models.CASCADE)
    tab_pk = models.ForeignKey(Tab, on_delete=models.CASCADE)
    type_pk = models.ForeignKey(Type, on_delete=models.DO_NOTHING)
    note_index = models.IntegerField(default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    content = models.TextField()
    color = models.CharField(max_length=10, default="f8f1ba")
    lock = models.BooleanField(default=False)

class History(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    board_id = models.IntegerField()    # If you have a chance to reset all database, change this to board_pk with ForeignKey.
    tab_index = models.IntegerField()
    note_index = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    type_index = models.IntegerField(default=1)
    content = models.TextField()
    color = models.CharField(max_length=10, default="f8f1ba")
    date = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=True)

class Capsule(models.Model):
    user_pk = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    type_index = models.IntegerField()
    content = models.TextField()
    color = models.CharField(max_length=10, default="f8f1ba")

class Time_Machine(models.Model):
    board_pk = models.ForeignKey(Board, on_delete=models.CASCADE)   # Unlike History Table, All TimeMachines should be eliminated when Table is Deleted
    tab_index = models.IntegerField()
    tm_index = models.IntegerField()
    capsule_list = models.ManyToManyField(Capsule, related_name="time_machine")
    created_at = models.DateTimeField(auto_now_add=True)
