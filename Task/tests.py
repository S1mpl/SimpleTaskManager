from django.test import TestCase, Client
from User.models import User
from Project.models import Project
from Task.models import Task

class TaskTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('warsss@mail.by', 'password')
        cls.manager = User.objects.create_manager('mng@mng.by', 'password')
        cls.developer = User.objects.create_developer('dev@dev.by', 'password')
        cls.project = Project(title='testproject', description='testdesc',  due_date='2222-12-22')
        cls.project.save()
        cls.project.users.add(cls.admin)
        cls.project.users.add(cls.manager)
        cls.project.users.add(cls.developer)
        cls.task = Task(title='1', description='asdasd', project=cls.project, priority=1, create_manager=cls.manager, developer=cls.developer, due_date='2222-12-22')
        cls.task.save()

    def test_view_page(self):
        c = Client()
        #no login
        c = Client()
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/task/1/add/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/project/1/task/1/edit/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/task/1/delete/')
        self.assertEqual(response.status_code, 302)
        #admin
        c.login(username='warsss@mail.by', password='password')
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/add/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/1/edit/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/1/delete/')
        self.assertEqual(response.status_code, 200)
        c.logout()
        #manager
        c.login(username='mng@mng.by', password='password')
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/add/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/1/edit/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/1/delete/')
        self.assertEqual(response.status_code, 200)
        c.logout()
        # developer
        c.login(username='dev@dev.by', password='password')
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/task/add/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/task/1/edit/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/task/1/delete/')
        self.assertEqual(response.status_code, 302)
        c.logout()

