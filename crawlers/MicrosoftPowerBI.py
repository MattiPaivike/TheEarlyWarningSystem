from .WebCrawlerSettings import *

#main variables
name = "Microsoft Power BI Desktop"
url = "https://www.microsoft.com/en-us/download/details.aspx?id=58494"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = False
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = ""

New_App = False
#################################

def crawl_data(url):
    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    return page_soup

#######################################

def crawl_version(data):

    divs = data.findAll("p")

    r = '\d\.\d\d\.\d*\.\d*'

    versions_list = re.findall(r, str(divs))

    return versions_list

################################################################
