from datetime import datetime
from threading import Thread
import time
from app import app, db
from models import Reminder, Task

# This would typically involve integrating with an email or SMS service. Here is a simplified example that could be expanded:

def send_notification(reminder):
    print(f"Sending {reminder.notification_method} notification for Task ID {reminder.task_id} at {reminder.remind_at}")

def reminder_worker():
    while True:
        now = datetime.now()
        reminders_to_send = Reminder.query.filter(Reminder.remind_at <= now, Reminder.sent == False).all()
        
        for reminder in reminders_to_send:
            send_notification(reminder)
            reminder.sent = True
            db.session.commit()
        
        time.sleep(60)

Thread(target=reminder_worker, daemon=True).start()
