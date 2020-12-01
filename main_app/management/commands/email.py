from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.core.mail import EmailMessage
from main_app.models import Software, Version
from users.models import CustomUser, Subscriptions
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

import sys
import logging
from datetime import datetime

import os
import json
import platform

def custom_log(message):
    #get operating System and define paths
    if platform.system() == 'Windows':
        path_log = '\\logging\\'
        path_part = '\\'
    else:
        path_log = '/logging'
        path_part = '/'

    #define logfilename
    logfilename = "email.log"
    folder_path = sys.path[0] + path_log + path_part
    completeName = folder_path + logfilename

    #create folder if not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #print("date and time =", dt_string)

    #log full message
    message = "\n" + str(now) + ": " + message

    f = open(completeName, "a")
    f.write(message)
    f.close()


if platform.system() == 'Windows':
    path = 'c:\\temp\\config.json'
else:
    path = '/etc/config.json'

with open(path) as config_file:
    config = json.load(config_file)


class Command(BaseCommand):
    help = 'main email sending function'

    def add_arguments(self, parser):
        parser.add_argument('job_type', type=str, help='type of job', nargs='?', default="")
        parser.add_argument('error_type', type=str, help='type of error', nargs='?', default="")
        parser.add_argument('errors', type=str, help='list of detected errors', nargs='?', default="")
        parser.add_argument('app_name', type=str, help='application name', nargs='?', default="")
        parser.add_argument('app_version', type=str, help='application version', nargs='?', default="")
        parser.add_argument('app_website', type=str, help='application website', nargs='?', default="")
        parser.add_argument('user_email', type=str, help='user email', nargs='?', default="")
        parser.add_argument('activation_key', type=str, help='activation key', nargs='?', default="")
        parser.add_argument('contact_text', type=str, help='contact', nargs='?', default="")
        parser.add_argument('dllink_x86', type=str, help='dllink_x86', nargs='?', default="")
        parser.add_argument('dllink_x64', type=str, help='dllink_x64', nargs='?', default="")
        parser.add_argument('dllink', type=str, help='dllink', nargs='?', default="")
        parser.add_argument('checksum_x86', type=str, help='checksum_x86', nargs='?', default="")
        parser.add_argument('checksum_x64', type=str, help='checksum_x64', nargs='?', default="")
        parser.add_argument('checksum', type=str, help='checksum', nargs='?', default="")

    def handle(self, *args, **kwargs):

        #arguments
        job_type = kwargs['job_type']
        error_type = kwargs['error_type']
        errors = kwargs['errors']
        app_name = kwargs['app_name']
        app_version = kwargs['app_version']
        app_website = kwargs['app_website']
        user_email = kwargs['user_email']
        activation_key = kwargs['activation_key']

        contact_text = kwargs['contact_text']
        dllink_x86 = kwargs['dllink_x86']
        dllink_x64 = kwargs['dllink_x64']
        dllink = kwargs['dllink']

        checksum_x86 = kwargs['checksum_x86']
        checksum_x64 = kwargs['checksum_x64']
        checksum = kwargs['checksum']

        admin_email = config['ADMIN_EMAIL']

        #get operating System and define paths
        if platform.system() == 'Windows':
            path_part = '\\'
        else:
            path_part = '/'

        custom_log('Starting email function with the following arguments. Job type: ' + job_type + ' Activationkey: ' + activation_key + ' Error type: ' + error_type + ' Errors: ' + str(errors) + ' App_name: ' + app_name + ' App_version ' + app_version)
        email_list = []
        if job_type == "new_version":
            custom_log("Compiling new version email for application: " + app_name + " version: " + app_version)
            subject = "Version " + app_version + " of application: " + app_name + " has been released!"
            #search subscriptions and append users
            subscriptions = Subscriptions.objects.filter(app_subscriptions=app_name)
            if subscriptions:
                for sub in subscriptions:
                    custom_log('found app ' + app_name + ' in users: ' + str(sub.user) + ' subscriptions. Appending user to email list.')
                    email_list.append(str(sub.user))

        if job_type == "error":
            custom_log("Compiling error email for error type: " + error_type)
            email_list.append(admin_email)
            if error_type == "crawler":
                subject = "ERROR crawling website for " + app_name
                body = errors
            if error_type == "process_data":
                subject = "ERROR processing data for " + app_name
                body = errors

        if job_type == "activation":
            custom_log("Compiling activation email for user: " + user_email + " with activation link: https://www.earlywarningsys.net/activation/"+activation_key)
            email_list.append(user_email)
            subject = "Email activation link for the Early Warning System"
            body = "https://www.earlywarningsys.net/activation/"+activation_key

        if job_type == "Run_all":
            custom_log("Compiling Run_All complete email")
            email_list.append(admin_email)
            subject = "The Early Warning System Run_all job complete"
            body = "Your scheduled task seems to work properly. \n\nAll Scripts seem to be in order. \n\nMaybe adding some more stuff to this email in the future. \n\nThe Early Warning System Team."

        if job_type == "contact":
            custom_log("Compiling contact email")
            email_list.append(admin_email)
            subject = "User: " + str(user_email) + " sent a contact form!"
            user_text = str(user_email)
            body = contact_text

        if job_type == "New_App":
            custom_log("Compiling new application announcement email")
            email_list.append(admin_email)
            subject = "New software: " + app_name + " has been added to the Early Warning System for tracking!"
            AllUsers = CustomUser.objects.all()
            for u in AllUsers:
                if u.is_active == True:
                    email_list.append(str(u))
            body = "If you would like to receive email notifications for this new software then please sign in to your account and select the software for tracking."

        if job_type == "announcement":
            custom_log("Compiling announcement email")
            email_list.append(admin_email)
            subject = "This is an Early Warning System Announcement!"
            AllUsers = CustomUser.objects.all()
            for u in AllUsers:
                if u.is_active == True:
                    email_list.append(str(u))

        email_count = 0

        if email_list:
            #convert email list to set and back to avoid sending duplicate emails
            email_list = set(email_list)
            email_list = list(email_list)
            for email_rec in email_list:
                custom_log("Sending email to: " + str(email_rec))
                if job_type != "announcement":
                    html_message = render_to_string('main_app' +  path_part + 'mail_template.html', locals())
                else:
                    html_message = render_to_string('main_app' + path_part + 'mail_template_announcement.html', locals())
                body_stripped = strip_tags(html_message)
                from_email = 'noreply@earlywarningsys.net'
                to = email_rec
                send_mail(subject, body_stripped, from_email, [to], html_message=html_message)
                email_count += 1

            custom_log('Email job completed. Sent a total of: ' + str(email_count) + ' emails')

        else:
            custom_log('No users seem to have subscribed to software: ' + str(app_name) + ' will not send email.')
