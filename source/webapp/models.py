from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Title')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description project')
    status = models.ForeignKey('webapp.ProjectStatus', related_name='tracker', on_delete=models.PROTECT,
                               verbose_name='Project status', blank=False, null=True, default='active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Time updated')


    def __str__(self):
        return self.title


class ProjectStatus(models.Model):
    status_project = models.CharField(max_length=40, null=False, blank=False, verbose_name='Project status')

    def __str__(self):
        return self.status_project


def get_admin():
    return User.objects.get(username='admin').id


class Tracker(models.Model):
    created_by = models.ForeignKey(User, null=False, blank=False, default=get_admin, verbose_name='created by',
                                   on_delete=models.PROTECT, related_name='tracker_by')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name='tracker_assigned', verbose_name='assigned to')
    summary = models.TextField(max_length=100, null=False, blank=False, verbose_name='Summary')
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name='Description')
    status = models.ForeignKey('webapp.Status', related_name='tracker', on_delete=models.PROTECT, verbose_name='Status')
    type = models.ForeignKey('webapp.Type', related_name='tracker', on_delete=models.PROTECT, verbose_name='Type')
    project_id = models.ForeignKey('webapp.Project', related_name='tracker',
                                   on_delete=models.SET_NULL, verbose_name='Project', blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of add')

    def __str__(self):
        return self.summary


class Type(models.Model):
    type = models.CharField(max_length=40, null=False, blank=False, verbose_name='Type')

    def __str__(self):
        return self.type


class Status(models.Model):
    status = models.CharField(max_length=40, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return self.status


class Team(models.Model):
    project = models.ForeignKey('webapp.Project', related_name='team_user',
                                on_delete=models.CASCADE, verbose_name='Project')
    user = models.ForeignKey('auth.User', related_name='user_team', on_delete=models.CASCADE, verbose_name='user')
    updated_at = models.DateTimeField(auto_now=False, blank=True, null=True,  verbose_name='Date of completion')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')

    def __str__(self):
        return f'{self.project} - {self.user}'
