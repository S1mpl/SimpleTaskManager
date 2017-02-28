from django.db import models
from datetime import datetime
from Project.models import Project
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateTimeField()
    developer = models.ForeignKey(User, verbose_name='Разработчик')
    project = models.ForeignKey(Project,verbose_name='Проект')
    files = models.FileField(upload_to='upload/',verbose_name='Прикрепленные файлы')

    def save(self, *args, **kwargs):
        try:
            this_task = Task.objects.get(pk = self.pk)
            if this_task.files != self.files:
                this_task.files.delete(save=False)
        except:
            pass
        super(Task, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.files.delete(save=False)
        super(Task, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'