from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_recurrence_job():
    os.system('python ./handleRecurrance.py')

scheduler = BlockingScheduler()
scheduler.add_job(handle_recurrence_job, 'interval', days=1)  # or use CronTrigger

if __name__ == '__main__':
    try:
        logging.info('Starting scheduler...')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
