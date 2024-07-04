from django.core.management import BaseCommand

from mail_app.utils import my_period_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        my_period_mail()

