from .WebCrawlerSettings import *

#main variables
name = "Wireshark"
url = "https://www.wireshark.org/download.html"

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

    r = 'current stable release of Wireshark is \d\.\d\.\d*'

    repElemList = data.find("div", {"class": "ws-well"})

    result = re.search(r, str(repElemList))
    version_text = (str(result.group(0)))
    version_text = version_text.replace('current stable release of Wireshark is ', '')

    versions_list.append(version_text)

    return versions_list

#########################################################
def crawl_dllink_x64(version, data):

    div = data.find("div",{"id":"group_accordion_stable"})

    links = div.findAll("a")

    for link in links:
        if "Windows Installer (64-bit)" in link:
            dllink_64 = link.get("href")
        if "Windows Installer (32-bit)" in link:
            dllink_32 = link.get("href")

    dllink_64 = dllink_64.replace(".exe", ".msi")
    dllink_32 = dllink_32.replace(".exe", ".msi")

    return dllink_64
########################################################

def crawl_dllink_x86(version, data):

    div = data.find("div",{"id":"group_accordion_stable"})

    links = div.findAll("a")

    for link in links:
        if "Windows Installer (64-bit)" in link:
            dllink_64 = link.get("href")
        if "Windows Installer (32-bit)" in link:
            dllink_32 = link.get("href")

    dllink_64 = dllink_64.replace(".exe", ".msi")
    dllink_32 = dllink_32.replace(".exe", ".msi")

    return dllink_32

########################################################

def crawl_checksum_x64(version, data):

    checksum_url = "https://www.wireshark.org/download/SIGNATURES-" + version + ".txt"

    #navigate to checksum url
    req = Request(url=checksum_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #split readme file to lines for looping
    lines = str(page_soup).split("\n")

    for line in lines:
        if version + ".msi" in line and "SHA256" in line and "win32" in line:
            checksum_32 = line
            checksum_32 = checksum_32.split("=")
            checksum_32 = checksum_32[1]
        if version + ".msi" in line and "SHA256" in line and "win64" in line:
            checksum_64 = line
            checksum_64 = checksum_64.split("=")
            checksum_64 = checksum_64[1]

    return checksum_64

########################################################

def crawl_checksum_x86(version, data):

    checksum_url = "https://www.wireshark.org/download/SIGNATURES-" + version + ".txt"

    #navigate to checksum url
    req = Request(url=checksum_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #split readme file to lines for looping
    lines = str(page_soup).split("\n")

    for line in lines:
        if version + ".msi" in line and "SHA256" in line and "win32" in line:
            checksum_32 = line
            checksum_32 = checksum_32.split("=")
            checksum_32 = checksum_32[1]
        if version + ".msi" in line and "SHA256" in line and "win64" in line:
            checksum_64 = line
            checksum_64 = checksum_64.split("=")
            checksum_64 = checksum_64[1]

    return checksum_32

########################################
