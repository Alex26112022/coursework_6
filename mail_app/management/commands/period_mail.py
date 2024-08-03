import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from mail_app.utils import my_period_mail, my_send_status

logger = logging.getLogger(__name__)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler1 = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler1.add_jobstore(DjangoJobStore(), "default1")

        scheduler2 = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler2.add_jobstore(DjangoJobStore(), "default2")

        scheduler1.add_job(
            my_period_mail,
            trigger=IntervalTrigger(days=1),
            id="my_job_mail_period",
            max_instances=1,
            replace_existing=True,
        )

        scheduler2.add_job(
            my_send_status,
            trigger=IntervalTrigger(minutes=5),
            id="my_job_status",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler1.start()
            scheduler2.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler1.shutdown()
            scheduler2.shutdown()
            logger.info("Scheduler shut down successfully!")
