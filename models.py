from datetime import datetime, timedelta
from app import db

class Task(db.Model):

    # table name
    __tablename__ = 'tasks'

    #Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    due_date = db.Column(db.Date)
    priority = db.Column(db.String(50))
    status = db.Column(db.String(64), default='incomplete')
    cancelled = db.Column(db.Boolean, default=False)
    reminder = db.Column(db.Date)
    recurring = db.Column(db.String(64))  # e.g., 'daily', 'weekly', 'custom'
    recurring_interval = db.Column(db.Integer)  # e.g., 1 for daily, 7 for weekly
    next_occurrence = db.Column(db.Date)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority,
            'status': self.status,
            'cancelled': self.cancelled,
            'reminder': self.reminder,
            'recurring': self.recurring,
            'recurring_interval': self.recurring_interval,
            'next_occurrence': self.next_occurrence
        }

    def update_next_occurrence(self):
        if self.recurring == 'Daily':
            self.next_occurrence = self.due_date + timedelta(days=1)
        elif self.recurring == 'Weekly':
            self.next_occurrence = self.due_date + timedelta(weeks=1)
        elif self.recurring == 'Custom'and self.recurring_interval is not None:
            self.next_occurrence = self.due_date + timedelta(days=self.recurring_interval)
        else :
            self.next_occurrence = None

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    remind_at = db.Column(db.DateTime, nullable=False)
    notification_method = db.Column(db.String(50), nullable=False)  # e.g., 'email', 'sms'
    sent = db.Column(db.Boolean, default=False)

    task = db.relationship('Task', backref=db.backref('reminders', lazy=True))