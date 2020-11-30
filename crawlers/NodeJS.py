from .WebCrawlerSettings import *

#main variables
name = "Node.js (Current)"
url = "https://nodejs.org/en"

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

    r = '\d{0,2}\.\d{0,2}\.\d{0,2} Current'

    repElemList = data.findAll("a", {"class": "home-downloadbutton"})

    versions_list = re.findall(r, str(repElemList))
    versions_list = [w.replace(' Current', '') for w in versions_list]


    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    dllink_32 = "https://nodejs.org/dist/latest/node-v" + version + "-x86.msi"

    return dllink_32
########################################################

def crawl_dllink_x64(version, data):

    dllink_64 = "https://nodejs.org/dist/latest/node-v" + version + "-x64.msi"

    return dllink_64
########################################################

def crawl_checksum_x86(version, data):
    url = "https://nodejs.org/dist/latest/SHASUMS256.txt"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    lines = str(page_soup).split("\n")

    for line in lines:
        if "node-v" + version + "-x64.msi" in line:
            checksum_64 = line.split(" ")[0]
        if "node-v" + version + "-x86.msi" in line:
            checksum_32 = line.split(" ")[0]
            checksum_32 = checksum_32.strip()

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):
    url = "https://nodejs.org/dist/latest/SHASUMS256.txt"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    lines = str(page_soup).split("\n")

    for line in lines:
        if "node-v" + version + "-x64.msi" in line:
            checksum_64 = line.split(" ")[0]
            checksum_64 = checksum_64.strip()
        if "node-v" + version + "-x86.msi" in line:
            checksum_32 = line.split(" ")[0]
            checksum_32 = checksum_32.strip()

    return checksum_64
#########################################################
