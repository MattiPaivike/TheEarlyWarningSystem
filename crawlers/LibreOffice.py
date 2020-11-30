from .WebCrawlerSettings import *

#main variables
name = "LibreOffice"
url = "https://www.libreoffice.org/download/download/"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = True
find_dllink_x64 = True

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

    repElemList = data.findAll("span", {"class": "dl_version_number"})

    versions_list = []

    for ver in repElemList:
        versions_list.append(ver.text)

    versions = [ verparse.parse(str(x)) for x in versions_list ]

    version = max(versions)

    version = str(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    dllink_x86 = "https://download.documentfoundation.org/libreoffice/stable/" + version + "/win/x86/LibreOffice_" + version + "_Win_x86.msi"

    return dllink_x86
#########################################################
def crawl_dllink_x64(version, data):
    dllink_x64 = "https://download.documentfoundation.org/libreoffice/stable/" + version + "/win/x86_64/LibreOffice_" + version + "_Win_x64.msi"

    return dllink_x64
########################################################
