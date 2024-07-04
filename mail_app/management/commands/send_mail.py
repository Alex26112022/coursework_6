from django.core.management import BaseCommand

from mail_app.utils import main_mail


class Command(BaseCommand):
    def handle(self, *args, **options):
        main_mail()
