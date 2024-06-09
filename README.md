# Steps to run the application

### Todo-flask-api

Backend application starts on http://localhost:5010 .
App contains the necessary db models and api routes to handle to the todo application operations.

### Steps to start api service

### Update your postgres db configuration in config.py and dbUtils.py files respectively

Create a virtual env
python -m venv "<virtual env name>"

Activate the virtual env
source env-name/Scripts/activate

Run pip install to install the necessary requirements
pip install -r requirements.txt

Run commands to add database migation
flask db upgrade

Run the flask application
python app.py

#### handleRecurrance.py

Handles creation of new tasks based on next reccurance of the tasks. This can be run as cron job to handle from backend

#### notificationService.py

Handles sending user defined notifications. Can be improved by intergrating different notification tools.
Need better details on how notification can be handled.

## Scope of Improvements

1. Allow for reminders based on priority.
2. If recurrance is updated to none then delete the upcoming tasks scheduled.
3. Handle user reminder better by giving the option of remind based on different criteria like priority, schedule reminders , custom
4. Improve UI to show tabs for different Kinds of events Completed, Cancelled, Upcoming , All Tasks
5. Give filters to show tasks based on different criteria like date , priority, completion status etc
6. Give option to serach todo by name or description
7. on Deletion of task give user the option to delete upcoming recurrance as well and same for cancel.
