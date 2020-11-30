from .WebCrawlerSettings import *

#main variables
name = "Adobe Air"
url = "https://get.adobe.com/air/"

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

    divs = data.findAll("div", {"id": "autoSelectedVersion"})

    for div in divs:
        a = div.find("strong")

    result = a.text
    result = str(result).replace("Version ", "")
    versions_list.append(result)

    return versions_list

################################################################
