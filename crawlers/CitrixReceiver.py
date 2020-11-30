from .WebCrawlerSettings import *

#main variables
name = "Citrix Receiver"
url = "https://www.citrix.com/downloads/citrix-receiver/windows/receiver-for-windows-latest.html"

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
    divs  = data.find("div", {"class": "ctx-text-content"})
    h1 = divs.find("h1")

    versions_list = []

    version = h1.text
    version = version.replace("Receiver ","")
    version = version.replace(" for Windows","")

    versions_list.append(version)

    return versions_list

################################################################
