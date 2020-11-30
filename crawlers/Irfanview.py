from .WebCrawlerSettings import *

#main variables
name = "Irfanview"
url = "https://www.irfanview.com/"

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

    repElemList = data.find("div", {"id": "download-desc"})
    repElemID = repElemList.find('strong')
    version_text =(repElemID.text)

    version_text = version_text.replace('version', '')

    version = version_text.strip()

    versions_list.append(version)

    return versions_list

################################################################
