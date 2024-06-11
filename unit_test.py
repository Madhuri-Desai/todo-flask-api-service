import json
import unittest
from datetime import datetime, timedelta

from app import create_app
from models import Task,db
import requests

BASE_URL ='http://localhost:5010'

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/todo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_task(self):
        response = requests.post(BASE_URL+'/addTask', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_tasks(self):
        requests.post(BASE_URL+'/addTask', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        response = requests.get(BASE_URL+'/getAllTasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Sample Task')

    def test_create_reminder(self):
        task_response = requests.post(BASE_URL+'/addTask', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        data = json.loads(task_response.text)
        task_id = data['id']

        reminder_response = requests.post(f'{BASE_URL}/tasks/{task_id}/reminders', json={
            'remind_at': '2024-06-14T15:56:00',
            'notification_method': 'email'
        })
        self.assertEqual(reminder_response.status_code, 200)

    def test_get_reminders(self):
        task_response = requests.post(BASE_URL+'/addTask', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        data = json.loads(task_response.text)
        task_id = data['id']

        requests.post(f'{BASE_URL}/tasks/{task_id}/reminders', json={
            'remind_at': '2024-06-14T15:56:00',
            'notification_method': 'email'
        })

        response = requests.get(f'{BASE_URL}/tasks/{task_id}/reminders')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['notification_method'], 'email')

    def test_update_next_occurrence(self):
        task = Task(
            title='Sample Task',
            description='Sample Description',
            due_date=datetime.strptime('2024-06-15', '%Y-%m-%d').date(),
            recurring='Daily'
        )
        db.session.add(task)
        db.session.commit()

        task.update_next_occurrence()
        self.assertEqual(task.next_occurrence, task.due_date + timedelta(days=1))

    def test_get_task_by_id(self):
        task_response = requests.post(BASE_URL+'/addTask', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        data = json.loads(task_response.text)
        task_id = data['id']

        response = requests.get(f'{BASE_URL}/getTask/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.text) 
        self.assertIsInstance(data, dict)
        self.assertEqual(data['title'], 'Sample Task')
        self.assertEqual(data['description'], 'Sample Description')
        self.assertEqual(data['due_date'], '2024-06-15')

if __name__ == '__main__':
    unittest.main()
