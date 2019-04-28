from main_app.models import Software, Version
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from users.models import CustomUser, Subscriptions

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from packaging import version as ver
import re
import logging

#THIS SCRIPT IS ONLY USED FOR DEBUGGING PURPOSES

class Command(BaseCommand):
    help = 'web crawler for 7zip'

    def handle(self, *args, **options):
        initial_version = False
        appname = "7zip"
        #logging
        logfilename = appname + '_crawler_logfile.log'
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        #define our main url
        url = "https://www.7-zip.org/"

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
                logging.info('there was an error writing in to the database: ' + str(err) + ' The script will stop running.')
                errors += ' There was an error writing in to the database: ' + str(err) + ' The script will stop running.'
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

        #read the website with uclient
        #try:
        #    logging.info('connecting to ' + url)
        #    uClient = uReq(url)
        #    page_html = uClient.read()
        #except Exception as err:
        #    logging.warning('There was an error connecting to ' + url + ' ' + str(err) + ' The script will stop running.')
        #    errors += ' There was an error connecting to ' + url + ' ' + str(err) + ' The script will stop running.'
        #    Error_var = True

        #uClient.close()

        #make our soup for parsing
        #logging.info('making the soup for url: ' + url)
        #page_soup = soup(page_html, "html.parser")

        #get all newsTitle items
        #mydivs = page_soup.findAll("td", {"class": "NewsTitle"})
        #page_string = str(mydivs)

        #parse newstitle items for version types with regex
        #logging.info('sniffing through the html for regex pattern')
        #versions = re.findall('\d\d\.\d\d', page_string)
        versions = ['36.00']

        #convert our version strings to version items
        Error_var = False

        try:
            versions = [ ver.parse(x) for x in versions ]
        except:
            logging.warning('There was a problem converting html data to version items.')
            errors += ' There was a problem converting html data to version items.'
            Error_var = True

        if Error_var != True:
            #store the highest version in our list and compare
            highest = max(versions)
            logging.info('found the following highest version: ' + str(highest))

            logging.info('comparing versions')
            if highest > current_version:
                logging.info('the version found online was greater. adding new software version to database')
                #get our software instance
                software_name = Software.objects.get(name=appname)
                #delete old version from database before commiting to new version
                delete_old = software_name.version_set.all()
                delete_old.delete()
                #finally save the new version
                save_version = Version(version=str(highest), software=software_name)
                save_version.save()
                #send email
                if initial_version != True:
                    call_command('email', 'new_version', '', '', appname, str(highest), url, '', '')
                else:
                    logging.info('This appears to be an inital versio entry. Will not send email')
            else:
                logging.info('did not find a newer version of ' + appname + ' The script wont do anything else for now')
        else:
            logging.info('Sending error email')
            call_command('email', 'error', 'crawler', errors, appname, '', '', '', '')
