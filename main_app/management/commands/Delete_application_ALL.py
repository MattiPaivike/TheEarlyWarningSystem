from main_app.models import Software, Version
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from users.models import CustomUser, Subscriptions

import sys
import logging


scriptdir = sys.path[0]

logfiledir = str(scriptdir) + "/Logfiles/"

class Command(BaseCommand):
    help = 'Delete application from database'

    def add_arguments(self, parser):
        parser.add_argument('appname', type=str, help='name of application')


    def handle(self, *args, **kwargs):
        #logging
        logfilename = logfiledir + "Delete_Application.log"
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

        appname = kwargs['appname']

        logging.info("Starting delete operation for application: " + appname)


        try:
            logging.info("Deleting application: " + appname)
            software_name = Software.objects.all()

            for soft in software_name:
                soft.delete()
        except Exception as err:
            logging.info("Failed to delete application from database: " + appname + " errors: " + str(err))
