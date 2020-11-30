from .WebCrawlerSettings import *

#main variables
name = "Keepass"
url = "https://keepass.info/integrity.html"

##################################################
#define main settings
find_dllink = True
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = False
find_checksum_x86 = False
find_checksum_x64 = False

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

    body = data.find("table", {"class": "tablebox ra_int_table"})

    version_data = body.find("th")

    if "KeePass" in version_data.text:
        version = version_data.text

    version = version.replace("KeePass ","")

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink(version, data):

    dllink = "https://netcologne.dl.sourceforge.net/project/keepass/KeePass%202.x/" + version + "/KeePass-" + version + ".msi"

    return dllink
########################################################

def crawl_checksum(version, data):
    body = data.find("table", {"class": "tablebox ra_int_table"})

    code = body.findAll("code")

    #use 8 index for .msi file hash
    checksum = (code[8]).text
    checksum = checksum.replace(" ","")

    return checksum
#########################################################
