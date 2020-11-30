from .WebCrawlerSettings import *

#main variables
name = "Citrix Receiver LTSR"
url = "https://www.citrix.com/fi-fi/downloads/citrix-receiver/windows-ltsr/receiver-for-windows-ltsr-latest.html"

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
    divs = data.findAll("div", {"class": "ctx-text-content"})

    for div in divs:
        h1 = div.find("h1")

    r = '\d\.\d\.\d\d\d\d'

    versions_list = re.findall(r, str(h1))

    return versions_list

##############################################
