from django.db import models
from django.utils import timezone


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    register_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    delete_flag = models.BooleanField(default=False)

    class Meta:
        db_table = 'project'


class Backlog(models.Model):
    pbl_id = models.IntegerField(default=0)
    pbl_name = models.CharField(max_length=100)
    pbl_sp = models.CharField(null=True, blank=True, max_length=10)
    register_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(default=timezone.now)
    delete_flag = models.BooleanField(default=False)
    pbl_priority = models.IntegerField(default=0, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pbl_sprint = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'backlog'


class OfferedSp(models.Model):
    user_name = models.CharField(max_length=10)
    user_sp = models.CharField(default=0, max_length=10)
    register_date = models.DateTimeField(default=timezone.now)
    backlog = models.ForeignKey(Backlog, on_delete=models.CASCADE)
    sp_count = models.IntegerField(default=0)  # sp_countフィールドの追

    class Meta:
        db_table = 'offered_sp'
