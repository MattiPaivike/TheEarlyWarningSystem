from .WebCrawlerSettings import *

#main variables
name = "VLC Media Player"
url = "https://www.videolan.org/vlc"

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

    divs = data.find("div", {"id": "downloadDetails"})

    r = '\d\.\d\.\d{1,2}\.{0,1}\d{0,1}'

    versions_list = re.findall(r, str(divs))

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    dllink32 = "https://mirrors.dotsrc.org/vlc/vlc/" + version + "/win32/vlc-" + version + "-win32.msi"

    return dllink32
#########################################################
def crawl_dllink_x64(version, data):

    dllink64 = "https://mirrors.dotsrc.org/vlc/vlc/" + version + "/win64/vlc-" + version + "-win64.msi"

    return dllink64
########################################################

def crawl_checksum_x86(version, data):

    url = "https://mirrors.dotsrc.org/vlc/vlc/" + version + "/win32/vlc-" + version + "-win32.msi.sha256"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    checksum_32 = page_soup.text
    checksum_32 = checksum_32.strip()
    checksum_32 = checksum_32.split(" ")
    checksum_32 = checksum_32[0]

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):

    url = "https://mirrors.dotsrc.org/vlc/vlc/" + version + "/win64/vlc-" + version + "-win64.msi.sha256"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    checksum_64 = page_soup.text
    checksum_64 = checksum_64.strip()
    checksum_64 = checksum_64.split(" ")
    checksum_64 = checksum_64[0]

    return checksum_64
#########################################################
