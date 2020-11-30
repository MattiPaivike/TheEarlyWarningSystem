from main_app.models import Software, Version
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from users.models import CustomUser, Subscriptions

from packaging import version as ver
import sys
import re
import logging

scriptdir = sys.path[0]

logfiledir = str(scriptdir) + "/Logfiles/"


class Command(BaseCommand):
    help = 'Process all data'

    def add_arguments(self, parser):
        parser.add_argument('appname', type=str, help='name of application', nargs='?', default="")
        parser.add_argument('highest', type=str, help='highest version', nargs='?', default="")
        parser.add_argument('dllink', type=str, nargs='?', default="")
        parser.add_argument('dllink_x86', type=str, nargs='?', default="")
        parser.add_argument('dllink_x64', type=str, nargs='?', default="")
        parser.add_argument('checksum', type=str, nargs='?', default="")
        parser.add_argument('checksum_x86', type=str, nargs='?', default="")
        parser.add_argument('checksum_x64', type=str, nargs='?', default="")
        parser.add_argument('checksum_type', type=str, nargs='?', default="")

    def handle(self, *args, **kwargs):
        #logging
        logfilename_data = logfiledir + "Process_Data.log"
        logging.basicConfig(filename=logfilename_data,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

        errors = []

        #arguments
        appname = kwargs['appname']
        highest = kwargs['highest']
        dllink = kwargs['dllink']
        dllink_x86 = kwargs['dllink_x86']
        dllink_x64 = kwargs['dllink_x64']
        checksum = kwargs['checksum']
        checksum_x86 = kwargs['checksum_x86']
        checksum_x64 = kwargs['checksum_x64']
        checksum_type = kwargs['checksum_type']

        logging.info('Starting data processer job for app: ' + appname + ' version: ' + highest)

        #convert highest version to version item
        highest = ver.parse(highest)

        Error_var = False
        initial_version = False

        #check that our version contains only the characters we want
        if appname == 'DisplayLink':
            allowed_chars = set('1234567890.M ')
        else:
            allowed_chars = set('1234567890. ')
        if not set(str(highest)).issubset(allowed_chars):
            error_text = 'Version pattern contains illegal characters! something is wrong with the crawler!'
            logging.info(error_text)
            errors.append(error_text)
            Error_var = True
        else:
            Error_var = False


        if not Error_var:
            #first we need to check if our application exists in the database
            software_name = Software.objects.filter(name=appname)
            if not software_name:
                try:
                    logging.info('could not find: ' + appname + ' in the database. will create it' )
                    initial_version = True
                    current_version = ver.parse('0.0')
                    save_software = Software(name=appname)
                    save_software.save()

                except Exception as err:
                    error_text = ' There was an error writing in to the database: ' + str(err) + ' The script will stop running.'
                    logging.info(error_text)
                    errors.append(error_text)
                    Error_var = True

            else:
                logging.info('found ' + appname + ' in the database. checking for version' )
                try:
                    software_name = Software.objects.get(name=appname)
                    current_version = str(software_name.version_set.last())
                    if current_version:
                        current_version = ver.parse(current_version)
                        logging.info('current version in the database is: ' + str(current_version))
                except:
                    logging.info('The current version data for this app seems to be empty, setting version to  0.0')
                    current_version = ver.parse('0.0')
                    initial_version = True

            #special case for legacyversions
            if appname == "DisplayLink" or appname == "FileZilla":
                current_version = ver.LegacyVersion(str(current_version))
                highest = ver.LegacyVersion(str(highest))


            logging.info('comparing versions. current version is: ' + str(current_version) + ' and the new version is: ' + str(highest))
            if highest > current_version:
                logging.info('the version found online was greater. adding new software version to database')
                #get our software instance
                software_name = Software.objects.get(name=appname)
                #delete old version from database before commiting to new version
                if initial_version != True:
                    delete_old = software_name.version_set.all()
                    logging.info('deleting old version: ' + str(delete_old) + ' from the database')
                    delete_old.delete()
                #finally save the new version
                save_version = Version(version=str(highest), software=software_name)
                save_version.save()

                ############################################
                ##update Dllink and/or checksums to database

                versionset = software_name.version_set.last()

                if dllink:
                    versionset.dllink = dllink

                if dllink_x86:
                    versionset.dllink_x86 = dllink_x86

                if dllink_x64:
                    versionset.dllink_x64 = dllink_x64

                if checksum:
                    versionset.checksum = checksum

                if checksum_x86:
                    versionset.checksum_x86 = checksum_x64

                if checksum_x64:
                    versionset.checksum_x64 = checksum_x64

                if dllink or dllink_x86 or dllink_x64 or checksum or checksum_x86 or checksum_x64:
                    versionset.save()
                ############################################

                #send email
                if initial_version != True:
                    call_command('email', job_type=new_version, app_name=appname, app_version=str(highest), dllink=dllink, dllink_x86=dllink_x86, dllink_x64=dllink_x64)
                else:
                    logging.info('This appears to be an initial version entry. Will not send email')
            else:
                logging.info('did not find a newer version of ' + appname + ' The script wont do anything else for now')

        if Error_var == True:
            logging.info('Sending error email for data processer')
            call_command('email', job_type="error", error_type=process_data, errors=errors, app_name=appname)
