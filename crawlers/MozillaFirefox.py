from .WebCrawlerSettings import *

#main variables
name = "Mozilla Firefox"
url = "https://www.mozilla.org/en-US/firefox/organizations/all/"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = True
find_dllink_x64 = True

find_checksum = False
find_checksum_x86 = True
find_checksum_x64 = True

checksum_type = "SHA256"

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

    repElemList = data.findAll("html", class_="windows x86 no-js")

    for repElem in repElemList:
        repElemID = repElem.get('data-latest-firefox')
        versions_list.append(repElemID)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    dllink_x86 = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/" + version + "/win32/en-US/Firefox Setup " + version + ".msi"

    return dllink_x86
#########################################################
def crawl_dllink_x64(version, data):
    dllink_x64 = "https://download-installer.cdn.mozilla.net/pub/firefox/releases/"+ version + "/win64/en-US/Firefox Setup " + version + ".msi"

    return dllink_x64
########################################################

def crawl_checksum_x86(version, data):
    url = "http://releases.mozilla.org/pub/firefox/releases/" + version +  "/SHA256SUMS"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    lines = str(page_soup).split("\n")

    for line in lines:
        if "win32/en-US/Firefox Setup " + version + ".msi" in line:
            checksum_32_en_US = line.split(" ")[0]
            checksum_32_en_US = checksum_32_en_US.strip()
        if "win64/en-US/Firefox Setup " + version + ".msi" in line:
            checksum_64_en_US = line.split(" ")[0]

    return checksum_32_en_US
#########################################################

def crawl_checksum_x64(version, data):
    url = "http://releases.mozilla.org/pub/firefox/releases/" + version +  "/SHA256SUMS"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    lines = str(page_soup).split("\n")

    for line in lines:
        if "win32/en-US/Firefox Setup " + version + ".msi" in line:
            checksum_32_en_US = line.split(" ")[0]
        if "win64/en-US/Firefox Setup " + version + ".msi" in line:
            checksum_64_en_US = line.split(" ")[0]
            checksum_64_en_US = checksum_64_en_US.strip()

    return checksum_64_en_US
#########################################################
