from django.db import models
from datetime import datetime, timedelta
from Project.models import Project
from django.utils import timezone
from SimpleTaskManager import settings

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    priority = models.SmallIntegerField(verbose_name='Важность')
    is_active = models.BooleanField(default=True)
    due_date = models.DateTimeField(default=(timezone.now() + timedelta(weeks=1)))
    create_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Менеджер', related_name='manager', null=True)
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Разработчик', related_name='developer', null=True)
    project = models.ForeignKey(Project,verbose_name='Проект', null=True)
    date_create = models.DateTimeField(default=datetime.now(), verbose_name='Дата создания')

    class Meta:
        ordering = ['-is_active','-date_create']
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

class TaskFiles(models.Model):
    task = models.ForeignKey(Task)
    files = models.FileField(upload_to='task/%Y/%m', verbose_name='Файлы')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')


    def delete(self, *args, **kwargs):
        self.files.delete(save=False)
        super(TaskFiles, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'