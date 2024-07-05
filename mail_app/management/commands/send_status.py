from django.core.management import BaseCommand

from mail_app.utils import my_send_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        my_send_status()
