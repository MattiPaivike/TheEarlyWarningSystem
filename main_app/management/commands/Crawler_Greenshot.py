from .WebCrawlerSettings import *


class Command(BaseCommand):
    help = 'web crawler Greenshot'

    def handle(self, *args, **options):
        Error_var = False
        errors = []
        initial_version = False
        appname = "Greenshot"
        #logging
        #logfiledir variable and scriptdir variable are imported from WebCrawlerSettings
        logfilename = logfiledir + appname + ".log"
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        #define our main url
        url = "https://getgreenshot.org/downloads/"
        downloadURL = "https://getgreenshot.org/downloads/"

        #headers to mimick an actual uClient
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

        #read the website with uclient
        try:
            logging.info('connecting to ' + url)
            req = Request(url=url, headers=headers)
            page_html = uReq(req).read()
        except Exception as err:
            error_text = ' There was an error connecting to ' + url + ' ' + str(err) + ' The script will stop running.'
            logging.warning(error_text)
            errors.append(error_text)
            Error_var = True

        if Error_var != True:
            #make our soup for parsing
            logging.info('making the soup for url: ' + url)
            page_soup = soup(page_html, "html.parser")

            versions_list = []

            repElemList = page_soup.findAll("div")

            r = 'Greenshot-RELEASE-\d\.\d\.\d\d{0,1}\.{0,1}\d{0,1}\d{0,1}\d'

            for repElem in repElemList:
                temp_list = re.search(r, str(repElem.text))
                if temp_list:
                    versions_list.append(temp_list.group(0))

            versions_list = [w.replace('Greenshot-RELEASE-', '') for w in versions_list]

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
            call_command('process_data', appname, str(highest), downloadURL)
        else:
            logging.info('Sending error email')
            call_command('email', 'error', 'crawler', str(errors), appname, '', '', '', '')