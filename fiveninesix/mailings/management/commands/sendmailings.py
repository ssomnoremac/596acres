import sys
import traceback

from django.core.management.base import BaseCommand, CommandError

from mailings.models import DaysAfterWatcherOrganizerAddedMailing

from mailings.mailers import send_all, register_mailer, DaysAfterWatcherOrganizerAddedMailer

register_mailer(DaysAfterWatcherOrganizerAddedMailing, DaysAfterWatcherOrganizerAddedMailer)

class Command(BaseCommand):
    help = 'Send all applicable mailings'

    def handle(self, *args, **options):
        """Send all applicable mailings"""
        try:
            recipients = send_all()
            self.stdout.write('sent to %d recipients.\n' % len(recipients))
        except Exception:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('There was an exception while sending mailings')
