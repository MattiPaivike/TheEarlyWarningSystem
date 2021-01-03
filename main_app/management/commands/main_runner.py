from main_app.models import Software, Version
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from .WebCrawlerSettings import *
import crawlers

def custom_log(message):
    #get operating System and define paths
    if platform.system() == 'Windows':
        path_log = '\\logging\\'
        path_part = '\\'
    else:
        path_log = '/logging'
        path_part = '/'

    #define logfilename
    logfilename = "main_runner.log"
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

errors = []

class Command(BaseCommand):
    help = 'main runner task for running all webcrawlers'

    def handle(self, *args, **options):

        #get list of all imported modules
        all_modules = crawlers.__all__

        #logging settings
        #logfilename = logfiledir + "MainRunner" + ".log"
        #logging.basicConfig(filename=logfilename,level=custom_log,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        custom_log('Starting mainrunner task')

        #loop through all modules (web-crawlers)
        for module in all_modules:

            if "WebCrawlerSettings" not in str(module):
                #main variables
                initial_version = False
                Error_var = False

                dllink = ""
                dllink_x86 = ""
                dllink_x64 = ""

                checksum = ""
                checksum_x86 = ""
                checksum_x64 = ""

                checksum_type = ""

                data = ""
                appname = ""
                url = ""
                latest_versions = ""
                highest = ""

                #get crawler information
                appname = getattr(getattr(crawlers,module),"name")
                url = getattr(getattr(crawlers,module),"url")

                custom_log('Running web-crawler: ' + appname)

                #first we need to check if our application exists in the database
                software_name = Software.objects.filter(name=appname)

                #if software is not found, create it to database
                if not software_name:
                    initial_version = True
                    custom_log('could not find: ' + appname + ' in the database. will create it' )
                    save_software = Software(name=appname)
                    save_software.save()
                else:
                    software_name = Software.objects.get(name=appname)
                    current_version_check = software_name.version_set.last()
                    if current_version_check:
                        initial_version = False
                    else:
                        initial_version = True
                        #delete software if no version is found and go to initial version process
                        software_name.delete()

                #get initial data for crawler
                try:
                    data = getattr(getattr(crawlers,module),"crawl_data")(url)
                except Exception as err:
                    error_text = 'There was an error running data crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                    custom_log(error_text)
                    errors.append(error_text)
                    Error_var = True
                #crawl latest version of software
                try:
                    latest_versions = getattr(getattr(crawlers,module),"crawl_version")(data)
                except Exception as err:
                    error_text = 'There was an error running version crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                    custom_log(error_text)
                    errors.append(error_text)
                    Error_var = True

                if not data:
                    Error_var = True
                    error_text = 'There was an error running data crawler for ' + appname
                    custom_log(error_text)
                    errors.append(error_text)

                if not latest_versions:
                    Error_var = True
                    error_text = 'There was an error running version crawler for ' + appname + ' the versions_list appears to be empty'
                    custom_log(error_text)
                    errors.append(error_text)

                if Error_var == False:
                    #convert list of versions to version items
                    latest_versions = [ verparse.parse(str(x)) for x in latest_versions ]
                    #get highest version in list
                    highest = max(latest_versions)
                    #check that we find what we expect to find

                    if highest:
                        if appname == 'DisplayLink':
                            allowed_chars = set('1234567890.M ')
                        else:
                            allowed_chars = set('1234567890. ')
                        if not set(str(highest)).issubset(allowed_chars):
                            error_text = 'Version pattern contains illegal characters! something is wrong with the crawler!'
                            custom_log(error_text)
                            errors.append(error_text)
                            Error_var = True
                        else:
                            Error_var = False
                    else:
                        Error_var = True
                        error_text = 'The version webcrawler for ' + appname + ' returned null. Something is wrong with the crawler.'
                        custom_log(error_text)
                        errors.append(error_text)

                if Error_var == False:
                    software_name = Software.objects.get(name=appname)
                    #save initial version to database
                    if initial_version == True:
                        custom_log('This appears to be an initial version entry for application: ' + appname + ' saving version: ' + str(highest) + ' to the database.')
                        save_version = Version(version=str(highest), software=software_name)
                        save_version.save()

                    if initial_version == False:
                        #get latest version from database
                        current_version = str(software_name.version_set.last())
                        #change current version to version object
                        current_version = verparse.parse(current_version)
                        if appname == "DisplayLink" or appname == "FileZilla":
                            current_version = verparse.LegacyVersion(str(current_version))
                            highest = verparse.LegacyVersion(str(highest))
                        if highest <= current_version:
                            custom_log("The detected version: " + str(highest) + " for application: " + appname + "." + " Was not greater than the current version: " + str(current_version))
                        if highest > current_version:
                            custom_log("New version: " + str(highest) + " detected for: " + appname + "." + " and it was considered higher than the old version: " + str(current_version))
                    elif initial_version == True:
                        #set temporary version for initial version entry
                        current_version = verparse.parse("0.1")

                    if initial_version == True or highest > current_version:
                        if initial_version == True:
                            custom_log("Initial version detected for:" + appname)

                        #determine what data is available for this crawler
                        find_dllink = getattr(getattr(crawlers,module),"find_dllink")
                        find_dllink_x86 = getattr(getattr(crawlers,module),"find_dllink_x86")
                        find_dllink_x64 = getattr(getattr(crawlers,module),"find_dllink_x64")
                        find_checksum = getattr(getattr(crawlers,module),"find_checksum")
                        find_checksum_x86 = getattr(getattr(crawlers,module),"find_checksum_x86")
                        find_checksum_x64 = getattr(getattr(crawlers,module),"find_checksum_x64")

                        New_App = False
                        New_App = getattr(getattr(crawlers,module),"New_App")
                        checksum_type = getattr(getattr(crawlers,module),"checksum_type")

                        if find_dllink == True:
                            try:
                                dllink = getattr(getattr(crawlers,module),"crawl_dllink")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running dllink crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if "http" not in dllink:
                                if "ftp" not in dllink:
                                    Error_var = True
                                    check_error = "The download link for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + dllink

                        if find_dllink_x86 == True:
                            try:
                                dllink_x86 = getattr(getattr(crawlers,module),"crawl_dllink_x86")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running dllink_x86 crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if "http" not in dllink_x86:
                                Error_var = True
                                check_error = "The x86 download link for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + dllink_x86

                        if find_dllink_x64 == True:
                            try:
                                dllink_x64 = getattr(getattr(crawlers,module),"crawl_dllink_x64")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running dllink_x64 crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if "http" not in dllink_x64:
                                Error_var = True
                                check_error = "The x64 download link for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + dllink_x64

                        if find_checksum == True:
                            try:
                                checksum = getattr(getattr(crawlers,module),"crawl_checksum")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running checksum crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if checksum == "":
                                Error_var = True
                                check_error = "The checksum data for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + checksum

                        if find_checksum_x86 == True:
                            try:
                                checksum_x86 = getattr(getattr(crawlers,module),"crawl_checksum_x86")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running checksum_x86 crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if checksum_x86 == "":
                                Error_var = True
                                check_error = "The x86 checksum data for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + checksum_x86

                        if find_checksum_x64 == True:
                            try:
                                checksum_x64 = getattr(getattr(crawlers,module),"crawl_checksum_x64")(str(highest),data)
                            except Exception as err:
                                error_text = 'There was an error running checksum_x64 crawler for: ' + appname + "This error appeared: " + str(err) + ' The script will stop running.'
                                custom_log(error_text)
                                errors.append(error_text)
                                Error_var = True
                            if checksum_x64 == "":
                                Error_var = True
                                check_error = "The x64 checksum data for app: " + appname + " did not match the expected pattern. Could not commit to database. Here is the failed data: " + checksum_x64

                        #crawlers seem to be working, commit the data to the databse
                        if Error_var != True:

                            if initial_version != True:
                                delete_old = software_name.version_set.all()
                                custom_log('deleting old version: ' + str(delete_old) + ' from the database')
                                delete_old.delete()
                                #finally save the new version
                                custom_log('Commiting new version: ' + str(highest) + ' to the database.')
                                save_version = Version(version=str(highest), software=software_name)
                                save_version.save()

                            versionset = software_name.version_set.last()
                            now = datetime.now()
                            dt_string = now.strftime("%d/%m/%Y")
                            versionset.lastupdated = dt_string

                            if dllink:
                                custom_log('Saving dllink: ' + dllink + ' to the database.')
                                versionset.dllink = dllink

                            if dllink_x86:
                                custom_log('Saving dllink_x86: ' + dllink_x86 + ' to the database.')
                                versionset.dllink_x86 = dllink_x86

                            if dllink_x64:
                                custom_log('Saving dllink_x64: ' + dllink_x64 + ' to the database.')
                                versionset.dllink_x64 = dllink_x64

                            if checksum:
                                custom_log('Saving checksum: ' + checksum + ' to the database.')
                                versionset.checksum = checksum

                            if checksum_x86:
                                custom_log('Saving checksum_x86: ' + checksum_x86 + ' to the database.')
                                versionset.checksum_x86 = checksum_x86

                            if checksum_x64:
                                custom_log('Saving checksum_x64: ' + checksum_x64 + ' to the database.')
                                versionset.checksum_x64 = checksum_x64

                            if checksum_type != "":
                                custom_log('Saving checksum type: ' + checksum_type + ' to the database.')
                                versionset.checksum_type = checksum_type

                            if find_dllink or find_dllink_x86 or find_dllink_x64 or find_checksum or find_checksum_x86 or find_checksum_x64:
                                versionset.save()
                            else:
                                versionset.save()

                        else:
                            error_text = check_error
                            custom_log(error_text)
                            errors.append(error_text)
                            Error_var = True
                        #send email
                        if initial_version != True and Error_var != True:
                            print("placeholder")
                            #call_command('email', job_type="new_version", app_name=appname, app_version=str(highest), dllink=dllink, dllink_x86=dllink_x86, dllink_x64=dllink_x64, checksum=checksum, checksum_x86=checksum_x86, checksum_x64=checksum_x64)

                        if initial_version == True:
                            custom_log('This appears to be an initial version entry. Will not send email')
                            if New_App == True:
                                custom_log('This appears to be a New_App, sending announcement email.')
                                #call_command('email', job_type="New_App", app_name=appname,)

                if Error_var == True:
                    custom_log('Sending error email')
                    call_command('email', job_type="error", error_type="crawler", errors=errors, app_name=appname)
        custom_log('MainRunner Task Completed, sending email.')
        call_command('email', job_type="Run_all")
