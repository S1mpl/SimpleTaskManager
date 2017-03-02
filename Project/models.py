from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from SimpleTaskManager import settings


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(max_length=255, verbose_name='Описание')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Те кому домтупен проект')
    due_date = models.DateField(verbose_name='Срок проекта', db_index=True)
    is_active = models.BooleanField(default=True)
    date_create = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'