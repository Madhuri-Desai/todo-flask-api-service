import unittest
from datetime import datetime, timedelta
from app import app, db, Task, Reminder

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/todo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Task created')

    def test_get_tasks(self):
        self.app.post('/tasks', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Sample Task')

    def test_create_reminder(self):
        task_response = self.app.post('/tasks', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        task_id = task_response.get_json()['task']

        reminder_response = self.app.post(f'/tasks/{task_id}/reminders', json={
            'remind_at': '2024-06-14T15:56:00',
            'notification_method': 'email'
        })
        self.assertEqual(reminder_response.status_code, 200)
        data = reminder_response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Reminder created')

    def test_get_reminders(self):
        task_response = self.app.post('/tasks', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        task_id = task_response.get_json()['task']

        self.app.post(f'/tasks/{task_id}/reminders', json={
            'remind_at': '2024-06-14T15:56:00',
            'notification_method': 'email'
        })

        response = self.app.get(f'/tasks/{task_id}/reminders')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
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
        task_response = self.app.post('/tasks', json={
            'title': 'Sample Task',
            'description': 'Sample Description',
            'due_date': '2024-06-15',
            'recurring': 'Daily'
        })
        task_id = task_response.get_json()['task']

        response = self.app.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['title'], 'Sample Task')
        self.assertEqual(data['description'], 'Sample Description')
        self.assertEqual(data['due_date'], '2024-06-15')

if __name__ == '__main__':
    unittest.main()
