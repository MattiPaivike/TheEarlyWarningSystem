from users.models import CustomUser
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.mail import EmailMessage

import sys
import logging

scriptdir = sys.path[0]

logfiledir = str(scriptdir) + "/Logfiles/"

class Command(BaseCommand):
    help = 'Send mass emails to all users'

    def handle(self, *args, **kwargs):
        emails = CustomUser.objects.all()

        logfilename_massemail = logfiledir + "Send_Mass_Email.log"
        logging.basicConfig(filename=logfilename_massemail,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

        logging.info("Starting Mass email job")

        subject = "The Early Warning System Announcement"
        body = "This is a test email"

        for recipient in emails:
            logging.info("Sending email to: " + str(recipient.email))
            email = EmailMessage(
            subject,
            body,
            'noreply@earlywarningsys.net',
            [recipient.email],
            [],
            )

            try:
                email.send(fail_silently=False)
            except Exception as err:
                logging.info('there was an error sending email ' + str(err))
                raise CommandError
