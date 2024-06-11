from app import create_app
from models import Task,db
from datetime import datetime
import os

def create_recurring_tasks():
    print("Running Recurring task")
    now = datetime.now()
    recurring_tasks = Task.query.filter(Task.next_occurrence <= now).all()
    for task in recurring_tasks:
        new_task = Task(
            title=task.title,
            description=task.description,
            due_date=task.next_occurrence,
            priority=task.priority,
            status='incomplete',
            cancelled=False,
            reminder=task.reminder,
            recurring=task.recurring,
            recurring_interval=task.recurring_interval
        )
        new_task.update_next_occurrence()
        task.update_next_occurrence()
        print("Adding new task")
        db.session.add(new_task)
        db.session.commit()

if __name__ == '__main__':
    app = create_app('config.default')
    with app.app_context():
        create_recurring_tasks()