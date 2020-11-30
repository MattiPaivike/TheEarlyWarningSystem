from .WebCrawlerSettings import *

#main variables
name = "OpenOffice"
url = "http://www.openoffice.org/fi/download/"

##################################################
#define main settings
find_dllink = True
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = True
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

    r = '\d\.\d\.\d'

    repElemList = data.findAll("div", {"id": "announce"})

    versions_list = re.findall(r, str(repElemList))

    return versions_list

################################################################

def crawl_dllink(version, data):
    dllink32_en_US = "https://iweb.dl.sourceforge.net/project/openofficeorg.mirror/" + version +"/binaries/en-US/Apache_OpenOffice_" + version + "_Win_x86_install_en-US.exe"

    return dllink32_en_US
########################################################

def crawl_checksum(version, data):
    url = "https://downloads.apache.org/openoffice/" + version + "/binaries/en-US/Apache_OpenOffice_" + version + "_Win_x86_install_en-US.exe.sha256"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")
    checksum_32_en_US = str(page_soup).split(" ")[0]

    return checksum_32_en_US
#########################################################
