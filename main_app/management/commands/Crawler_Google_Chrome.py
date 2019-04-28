from .WebCrawlerSettings import *

class Command(BaseCommand):
    help = 'web crawler for Google Chrome'

    def handle(self, *args, **options):
        Error_var = False
        errors = []
        initial_version = False
        appname = "Google Chrome"
        #logging
        #logfiledir variable and scriptdir variable are imported from WebCrawlerSettings
        logfilename = logfiledir + appname + ".log"
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        #define our main url
        url = "https://omahaproxy.appspot.com/all.json"
        downloadurl = "https://www.google.com/chrome/"

        #read the website with uclient
        try:
            logging.info('connecting to ' + url)
            response = requests.get(url)
            json = response.json()
        except Exception as err:
            error_text = ' There was an error connecting to ' + url + ' ' + str(err) + ' The script will stop running.'
            logging.warning(error_text)
            errors.append(error_text)
            Error_var = True

        if Error_var != True:
            versions_list = []

            logging.info('sniffing through the json for version')
            versiondata = json[0]['versions'][4]['version']
            versions_list.append(versiondata)

            #if list empty. send error message
            if not versions_list:
                logging.info('The regex pattern did not seem to hit any matches. Something is wrong with your crawler.')
                Error_var = True
            else:
                Error_var = False
            #convert our version strings to version items
            try:
                versions = [ verparse.parse(str(x)) for x in versions_list ]
            except:
                error_text = ' There was a problem converting html data to version items.'
                logging.warning(error_text)
                errors.append(error_text)
                Error_var = True

        if Error_var != True:
            #store the highest version in our list and compare
            highest = max(versions)

            logging.info('Found the following highest version: ' + str(highest) + ' starting data processer')
            call_command('process_data', appname, str(highest), downloadurl)
        else:
            logging.info('Sending error email')
            call_command('email', 'error', 'crawler', str(errors), appname, '', '', '', '')
