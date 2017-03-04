import django
django.setup()
from celery.task import task
from Task.models import Task
from django.core.mail import send_mail
from SimpleTaskManager.settings import MANAGERS
from django.core.urlresolvers import reverse

@task(ignore_result=True)
def SendMail():
    tasks = Task.objects.filter(is_active=1).order_by('-developer')
    message = ''
    i=0
    pre_user = tasks[0].developer
    for task in tasks:
        if pre_user != task.developer:
            print(task.developer)
            send_mail('Ваши оставшиеся задачи', message, MANAGERS[0][1], [pre_user], fail_silently=False)
            pre_user = task.developer
            message = ''
            message += 'Проект: '+str(task.project.title) + ' Задача: <a href="' + \
                        str(reverse('task_detail', kwargs={"pk_project": task.project.id, 'pk': task.id})) + '">' + \
                        str(task.title) + '</a><br>'
        else:
            message += 'Проект: '+str(task.project.title) + ' Задача: <a href="' + \
                        str(reverse('task_detail', kwargs={"pk_project": task.project.id, 'pk': task.id})) + '">' + \
                        str(task.title) + '</a><br>'
            pre_user = task.developer
        i += 1
        if i == len(tasks):
            print(task.developer)
            send_mail('Ваши оставшиеся задачи', message, MANAGERS[0][1], [task.developer], fail_silently=False)