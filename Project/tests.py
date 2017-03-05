from django.test import TestCase, Client
from User.models import User
from Project.models import Project

class ProjectTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser('warsss@mail.by', 'password')
        cls.manager = User.objects.create_manager('mng@mng.by', 'password')
        cls.developer = User.objects.create_developer('dev@dev.by', 'password')
        cls.project = Project(title='testproject', description='testdesc',  due_date='2222-12-22')
        cls.project.save()
        cls.project.users.add(cls.admin)
        cls.project.users.add(cls.manager)

    def test_start_app_no_login(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/')
        self.assertEqual(response.status_code, 404)
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/add/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/edit/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/delete/')
        self.assertEqual(response.status_code, 302)


    def test_start_app_admin(self):
        c = Client()
        login = c.login(username='warsss@mail.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_start_app_manager(self):
        c = Client()
        login = c.login(username='mng@mng.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 200)

    def test_start_app_developer(self):
        c = Client()
        login = c.login(username='dev@dev.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/add/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/delete/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/edit/')
        self.assertEqual(response.status_code, 302)
        self.project.users.add(self.developer)
        response = c.get('/project/1/')
        self.assertEqual(response.status_code, 200)
        response = c.get('/project/1/delete/')
        self.assertEqual(response.status_code, 302)
        response = c.get('/project/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_admin_add_project(self):
        c = Client()
        login = c.login(username='warsss@mail.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/add/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/add/',{'title':'asd', 'description':'asdasd', 'due_date':'2222-12-22','users':1, 'users':2, 'users':3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/add/',{'title': 'asd', 'description': 'asdasd', 'users': 1, 'users': 2,'users': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/project/add/')
        response = c.post('/project/add/', {'title': 'asd',  'due_date':'2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/add/',{'description':'asdasd', 'due_date': '2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/project/add/')

    def test_admin_edit_project(self):
        c = Client()
        login = c.login(username='warsss@mail.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/1/edit/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/1/edit/',{'title':'asd', 'description':'asdasd', 'due_date':'2222-12-22','users':1, 'users':2, 'users':3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/',{'title': 'asd', 'description': 'asdasd', 'users': 1, 'users': 2,'users': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/', {'title': 'asd',  'due_date':'2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/',{'description':'asdasd', 'due_date': '2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')


    def test_admin_delete_project(self):
        c = Client()
        login = c.login(username='warsss@mail.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/1/delete/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')


    def test_manager_add_project(self):
        c = Client()
        login = c.login(username='mng@mng.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/add/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/add/',{'title': 'asd', 'description': 'asdasd', 'due_date': '2222-12-22', 'users': 1, 'users': 2, 'users': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/add/',{'title': 'asd', 'description': 'asdasd', 'users': 1, 'users': 2, 'users': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/project/add/')
        response = c.post('/project/add/', {'title': 'asd', 'due_date': '2222-12-22', 'users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/add/', {'description': 'asdasd', 'due_date': '2222-12-22', 'users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/project/add/')

    def test_manager_edit_project(self):
        c = Client()
        login = c.login(username='mng@mng.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/1/edit/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/1/edit/',{'title':'asd', 'description':'asdasd', 'due_date':'2222-12-22','users':1, 'users':2, 'users':3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/',{'title': 'asd', 'description': 'asdasd', 'users': 1, 'users': 2,'users': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/', {'title': 'asd',  'due_date':'2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')
        response = c.post('/project/1/edit/',{'description':'asdasd', 'due_date': '2222-12-22','users': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')


    def test_manager_delete_project(self):
        c = Client()
        login = c.login(username='mng@mng.by', password='password')
        self.assertEqual(login, True)
        response = c.get('/project/1/delete/')
        self.assertEqual(response.status_code, 200)
        response = c.post('/project/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/')





