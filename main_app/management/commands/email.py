from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.mail import EmailMessage
from main_app.models import Software, Version
from users.models import CustomUser, Subscriptions

import sys
import logging


import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

scriptdir = sys.path[0]

logfiledir = str(scriptdir) + "/Logfiles/"


class Command(BaseCommand):
    help = 'main email sending function'

    def add_arguments(self, parser):
        parser.add_argument('job_type', type=str, help='type of job')
        parser.add_argument('error_type', type=str, help='type of error')
        parser.add_argument('errors', type=str, help='list of detected errors')
        parser.add_argument('app_name', type=str, help='application name')
        parser.add_argument('app_version', type=str, help='application version')
        parser.add_argument('app_website', type=str, help='application website')
        parser.add_argument('user_email', type=str, help='user email')
        parser.add_argument('activation_key', type=str, help='activation key')

    def handle(self, *args, **kwargs):

        #logging
        logfilename_email = logfiledir + "Email.log"
        logging.basicConfig(filename=logfilename_email,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

        #arguments
        job_type = kwargs['job_type']
        error_type = kwargs['error_type']
        errors = kwargs['errors']
        app_name = kwargs['app_name']
        app_version = kwargs['app_version']
        app_website = kwargs['app_website']
        user_email = kwargs['user_email']
        activation_key = kwargs['activation_key']

        admin_email = config['ADMIN_EMAIL']

        logging.info('Starting email function with the following arguments. Job type: ' + job_type + ' Activationkey: ' + activation_key + ' Error type: ' + error_type + ' Errors: ' + errors + ' App_name: ' + app_name + ' App_version ' + app_version + ' App_website: ' + app_website)
        email_list = []
        if job_type == "new_version":
            logging.info("Compiling new version email for application: " + app_name + " version: " + app_version)
            subject = "Version " + app_version + " of application: " + app_name + " has been released!"
            body = "Version " + app_version + " of application: " + app_name + " has been released! \n\nDownload the new version from here: " + app_website + "\n\nThis email was brought to you by the Early Warning System."
            #search subscriptions and append users
            subscriptions = Subscriptions.objects.filter(app_subscriptions=app_name)
            if subscriptions:
                for sub in subscriptions:
                    logging.info('found app ' + app_name + ' in users: ' + str(sub.user) + ' subscriptions. Appending user to email list.')
                    email_list.append(str(sub.user))

        if job_type == "error":
            logging.info("Compiling error email for error type: " + error_type)
            email_list.append(admin_email)
            if error_type == "crawler":
                subject = "ERROR crawling website for " + app_name
                body = "The following errors appeared: " + errors
            if error_type == "process_data":
                subject = "ERROR processing data for " + app_name
                body = "The following errors appeared: " + errors

        if job_type == "activation":
            logging.info("Compiling activation email for user: " + user_email + " with activation link: https://www.earlywarningsys.net/activation/"+activation_key)
            email_list.append(user_email)
            subject = "Email activation link for the Early Warning System"
            body = "Here is your activation link for the Early Warning System. \n\nhttps://www.earlywarningsys.net/activation/"+activation_key+"\n\nClick the link above to activate your account. \n\nThe Early Warning System Team."

        if job_type == "Run_all":
            logging.info("Compiling Run_All complete email")
            email_list.append(admin_email)
            subject = "The Early Warning System Run_all job complete"
            body = "Your scheduled task seems to work properly. \n\nAll Scripts seem to be in order. \n\nMaybe adding some more stuff to this email in the future. \n\nThe Early Warning System Team."

        #send the email
        if email_list:
            for email_rec in email_list:
                logging.info("Sending email to: " + str(email_rec))
                email = EmailMessage(
                subject,
                body,
                'noreply@earlywarningsys.net',
                [email_rec],
                [],
                )

                try:
                    email.send(fail_silently=False)
                except Exception as err:
                    logging.info('there was an error sending email ' + str(err))
                    raise CommandError
        else:
            logging.info('No users seem to have subscribed to software: ' + str(app_name) + ' will not send email.')
