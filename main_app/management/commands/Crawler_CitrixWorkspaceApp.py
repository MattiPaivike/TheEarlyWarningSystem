from .WebCrawlerSettings import *

class Command(BaseCommand):
    help = 'web crawler for Citrix workspace app'

    def handle(self, *args, **options):
        Error_var = False
        errors = []
        initial_version = False
        appname = "Citrix Workspace app"
        #logfiledir variable and scriptdir variable are imported from WebCrawlerSettings
        logfilename = logfiledir + appname + ".log"
        logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')
        #define our main url
        url = "https://www.citrix.fi/downloads/workspace-app/windows/workspace-app-for-windows-latest.html"
        downloadURL = url

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

            r = "Citrix Workspace app \S* for Windows"

            logging.info('sniffing through the html for regex pattern')

            divs = page_soup.find("h1")

            versions_list = re.findall(r, str(divs))

            versions_list = [w.replace('Citrix Workspace app ', '') for w in versions_list]
            versions_list = [w.replace(' for Windows', '') for w in versions_list]


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