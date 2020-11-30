from .WebCrawlerSettings import *

#main variables
name = "Arcgis Pro"
url = "https://support.esri.com/en/technical-article/000012500"

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

    r = "Version \d\.\d{0,1}\.{0,1}\d{0,1}"

    versions_list = re.findall(r, str(data))

    versions_list = [w.replace('Version ', '') for w in versions_list]

    return versions_list

################################################################
