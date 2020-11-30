from .WebCrawlerSettings import *

#main variables
name = "Sublime Text"
url = "https://www.sublimetext.com/3"

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

    versions_list = []

    p = data.find("p", {"class": "latest"})

    version = p.text
    version = version.replace("Build ","")
    version = version.replace("Version: ","")

    versions_list.append(version)

    return versions_list

#########################################################
def crawl_dllink_x86(version, data):

    li32 = data.find("li", {"id": "dl_win_32"})

    li32 = li32.find("a")

    dllink32 = li32.get("href")

    return dllink32
########################################################

def crawl_dllink_x64(version, data):

    li64 = data.find("li", {"id": "dl_win_64"})

    li64 = li64.find("a")

    dllink64 = li64.get("href")

    return dllink64
########################################################
