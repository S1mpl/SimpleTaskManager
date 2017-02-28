from django.db import models
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    manager_create = models.ForeignKey(User, verbose_name='Менеджер')
    date_create = models.DateTimeField(default=datetime.now(), db_index=True, verbose_name='Дата создания')

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'