from datetime import datetime
from threading import Thread
import time
from models import  db
from app import create_app
from models import Reminder

# This would typically involve integrating with an email or SMS service. Here is a simplified example that could be expanded:
app = create_app("Notification")

def send_notification(reminder):
    print(f"Sending {reminder.notification_method} notification for Task ID {reminder.task_id} at {reminder.remind_at}")



def reminder_worker():
        with app.app_context():
            while True:
                now = datetime.now()
                print(f"Running notification service at {now}")
                try:
                    reminders_to_send = Reminder.query.filter(Reminder.remind_at <= now, Reminder.sent == False).all()
                    print(len(reminders_to_send))
                    for reminder in reminders_to_send:
                        send_notification(reminder)
                        reminder.sent = True
                        db.session.commit()
                except Exception as e:
                    print("Error fetching reminder list")
                    print(e)
                
                time.sleep(60)

Thread(target=reminder_worker, daemon=False).start()


