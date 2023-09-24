import dramatiq
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.controllers.messages_controller import MessagesController
api_logger = logging.getLogger(__name__)


@dramatiq.actor
def send_scheduled_message():
    MessagesController.send_whatsapp_message('')
    print(datetime.now())

def enable_scheduler():
    api_logger.info('called---------------')
    scheduler = BlockingScheduler()
    scheduler.add_job(
        send_scheduled_message.send,
        CronTrigger.from_crontab("* * * * *"),
    )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        scheduler.shutdown()