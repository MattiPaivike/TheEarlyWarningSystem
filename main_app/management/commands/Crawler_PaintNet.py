from .WebCrawlerSettings import *

class Command(BaseCommand):
    help = 'web crawler for Paint Net'

    def handle(self, *args, **options):
        Error_var = False
        errors = []
        initial_version = False
        appname = "Paint.NET"
        #logging
        #logfiledir variable and scriptdir variable are imported from WebCrawlerSettings
        logfilename = logfiledir + appname + ".log"
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        #define our main url
        url = "https://www.getpaint.net/download.html"
        downloadURL = url

        #special ssl cert check bypass for paintNET
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE


        #read the website with uclient
        try:
            logging.info('connecting to ' + url)
            with urllib.request.urlopen(url, context=ctx) as req:
                page_html = req.read()
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

            repElemList = page_soup.findAll("table", {"id": "table8"})

            #find the strong tags
            for repElem in repElemList:
                repElemID = repElem.find('strong')
                versions_list.append(repElemID.text)

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
