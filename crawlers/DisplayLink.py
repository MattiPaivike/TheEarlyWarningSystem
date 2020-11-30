from .WebCrawlerSettings import *

#main variables
name = "DisplayLink"
url = "https://www.displaylink.com/downloads/windows"

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

    versions_list = []

    repElemList = data.find("span", {"class": "download-version"})

    versions_list.append(repElemList.text)

    versions_list = [w.replace('Release: ', '') for w in versions_list]

    return versions_list

################################################################
