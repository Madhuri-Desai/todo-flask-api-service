import time
from app import create_app
from models import db, TodoItem
from datetime import datetime
import schedule

app = create_app()
app.app_context().push()

def create_recurring_tasks():
    now = datetime.now()
    recurring_tasks = TodoItem.query.filter(TodoItem.next_occurrence <= now).all()
    for task in recurring_tasks:
        new_task = TodoItem(
            title=task.title,
            description=task.description,
            due_date=task.next_occurrence,
            priority=task.priority,
            status='incomplete',
            canceled=False,
            reminder=task.reminder,
            recurring=task.recurring,
            recurring_interval=task.recurring_interval
        )
        new_task.update_next_occurrence()
        task.update_next_occurrence()
        db.session.add(new_task)
        db.session.commit()

def job():
    create_recurring_tasks()

schedule.every().hour.at(":00").do(job)
schedule.every().hour.at(":30").do(job)
# schedule.every(5).minutes.do(job)
# schedule.every().minute.at(":30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)