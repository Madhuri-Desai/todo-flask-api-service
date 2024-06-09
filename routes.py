from datetime import datetime
from flask import jsonify,request
from app import app, db
from models import Reminder, Task

def parse_datetime(datetime_str):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"Time data '{datetime_str}' does not match format '%Y-%m-%dT%H:%M:%S' or '%Y-%m-%dT%H:%M'")

@app.route('/getTask/<int:id>',methods = ['GET'])
def get_task(id):
    try:
        task = Task.query.get(id)
        if not task:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(task.to_dict())
    except Exception as e:
        return("Error fetching tasks",400)
    
@app.route('/getAllTasks',methods = ['GET'])
def get_tasks():
    try:
        tasks = Task.query.all()
        tasks_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date,
        'priority': task.priority,
        'status': task.status,
        'cancelled' : task.cancelled,
        'recurring': task.recurring,
        'recurring_interval' : task.recurring_interval,
        'next_occurrence' : task.next_occurrence
        } for task in tasks]
        response = jsonify(tasks_list)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return("Error fetching tasks",400)

    
@app.route('/addTask', methods=['POST'])
def add_task():    
    try:
        data = request.json
        todo = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
        priority=data.get('priority'),
        status=data.get('status', 'incomplete'),
        cancelled=data.get('cancelled', False),
        reminder=data['reminder'] if data.get('reminder') else None,
        recurring=data.get('recurring'),
        recurring_interval=data.get('recurring_interval')
        )
        if todo.recurring:
            todo.update_next_occurrence()
        db.session.add(todo)
        db.session.commit()
        return jsonify(todo.to_dict()), 201
    except Exception as e :
        return("Error adding task",500)


@app.route('/editTask/<int:id>', methods=['PUT'])
def edit_task(id):
    try:
        data = request.json
        todo = Task.query.get(id)
        if not todo:
            return jsonify({'error': 'Not found'}), 404
        todo.title = data.get('title', todo.title)
        todo.description = data.get('description', todo.description)
        todo.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else todo.due_date
        todo.priority = data.get('priority', todo.priority)
        todo.status = data.get('status', todo.status)
        todo.cancelled = data.get('cancelled', todo.cancelled)
        todo.reminder = datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('reminder') else todo.reminder
        todo.recurring = data.get('recurring', todo.recurring)
        todo.recurring_interval = data.get('recurring_interval', todo.recurring_interval)

        if todo.recurring:
            todo.update_next_occurrence()
        db.session.commit()
        return jsonify(todo.to_dict())
    except Exception as e:
        return("Error updating the task details",500)

@app.route('/updateTaskStatus/<int:id>', methods=['PUT'])
def update_task_status(id):
    try:
        data = request.json
        todo = Task.query.get(id)
        if not todo:
            return jsonify({'error': 'Not found'}), 404
        todo.status = data.get('status', todo.status)
        db.session.commit()
        return jsonify(todo.to_dict())
    except Exception as e:
        return("Error updating the task details",500)

@app.route('/updateTaskCancellation/<int:id>', methods=['PUT'])
def update_task_cancellation(id):
    try:
        data = request.json
        todo = Task.query.get(id)
        if not todo:
            return jsonify({'error': 'Not found'}), 404
        todo.status = data.get('cancelled', todo.cancelled)
        db.session.commit()
        return jsonify(todo.to_dict())
    except Exception as e:
        return("Error updating the task details",500)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        todo = Task.query.get(id)
        if not todo:
            return jsonify({'error': 'Not found'}), 404
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    except Exception as e:
        return("Error detelting the task",500)

@app.route('/tasks/<int:task_id>/reminders', methods=['POST'])
def create_reminder(task_id):
    try:
        data = request.json
        task = Task.query.get_or_404(task_id)
        remind_at = datetime.strptime(data['remind_at'], '%Y-%m-%dT%H:%M:%S')
        notification_method = data['notification_method']

        new_reminder = Reminder(task_id=task.id, remind_at=remind_at, notification_method=notification_method)
        db.session.add(new_reminder)
        db.session.commit()
        
        return jsonify({'message': 'Reminder created', 'reminder': new_reminder.id})
    except Exception as e:
        return("Error setting reminder",500)


@app.route('/tasks/<int:task_id>/reminders', methods=['GET'])
def get_reminders(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        reminders = Reminder.query.filter_by(task_id=task.id).all()
        
        reminders_list = [{
            'id': reminder.id,
            'remind_at': reminder.remind_at.isoformat(),
            'notification_method': reminder.notification_method,
            'sent': reminder.sent
        } for reminder in reminders]
        
        return jsonify(reminders_list)
    except Exception as e:
        return("Error fetching reminder for give task",500)
