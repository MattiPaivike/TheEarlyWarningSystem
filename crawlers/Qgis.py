from .WebCrawlerSettings import *

#main variables
name = "QGIS"
url = "https://qgis.org/en/site/forusers/download.html"

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

    r = '^\d\.\d{0,2}\.{0,1}\d{0,2}'

    repElemList = data.find("span", {"class": "navbar-text pull-left"})

    versions_list = re.findall(r, str(repElemList.text))

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    divs = data.find("div", {"id": "windows"})

    links = divs.findAll("a")

    links_list = []

    for link in links:
        if "QGIS Standalone Installer Version" in str(link) and "32 bit" in str(link):
            href = link.get("href")
            links_list.append(href)

    #get first link witch we expect to be 64bit latest release Version
    dllink_32 = links_list[0]

    return dllink_32
#########################################################
def crawl_dllink_x64(version, data):

    divs = data.find("div", {"id": "windows"})

    links = divs.findAll("a")

    links_list = []

    #get 64bit link
    for link in links:
        if "QGIS Standalone Installer Version" in str(link) and "64 bit" in str(link):
            href = link.get("href")
            links_list.append(href)

    #get first link witch we expect to be 64bit latest release Version
    dllink_64 = links_list[0]

    return dllink_64
########################################################

def crawl_checksum_x86(version, data):

    divs = data.find("div", {"id": "windows"})

    links = divs.findAll("a")

    links_list = []

    #get 64bit link
    for link in links:
        if "QGIS Standalone Installer Version" in str(link) and "32 bit" in str(link):
            href = link.get("href")
            links_list.append(href)

    dllink_32 = links_list[0]

    #split download link to get filename
    filename = dllink_32.split("/")
    filename = filename.pop()

    #use filename to find checksum url for 32bit installer
    for link in links:
        if str(filename) in str(link) and "sha256" in str(link):
            checksum_file = link.get("href")

    req = Request(url=checksum_file, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    checksum_32 = str(page_soup).split(" ")[0]

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):

    divs = data.find("div", {"id": "windows"})

    links = divs.findAll("a")

    links_list = []

    #get 64bit link
    for link in links:
        if "QGIS Standalone Installer Version" in str(link) and "64 bit" in str(link):
            href = link.get("href")
            links_list.append(href)

    dllink_64 = links_list[0]

    #split download link to get filename
    filename = dllink_64.split("/")
    filename = filename.pop()

    for link in links:
        if str(filename) in str(link) and "sha256" in str(link):
            checksum_file = link.get("href")

    ###CHECKSUM is a file! we download the file and get checksum
    req = Request(url=checksum_file, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    checksum_64 = str(page_soup).split(" ")[0]

    return checksum_64
#########################################################
