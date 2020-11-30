from .WebCrawlerSettings import *

#main variables
name = "R For Windows"
url = "https://cran.r-project.org/bin/windows/base"

##################################################
#define main settings
find_dllink = True
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = True
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = "MD5"

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

    h1 = data.find("h1")

    version = h1.text
    version = version.replace("R-", "")
    version = version.replace(" for Windows (32/64 bit)","")

    versions_list.append(version)

    return versions_list

#########################################################
def crawl_dllink(version, data):

    links = data.findAll("a")

    for link in links:
        if version in str(link) and "Download" in str(link):
            filename = link.get("href")
        if "fingerprint" in str(link):
            checksum_url = link.get("href")

    dllink = "https://cran.r-project.org/bin/windows/base/" + filename

    return dllink
########################################################

def crawl_checksum(version, data):

    links = data.findAll("a")

    for link in links:
        if version in str(link) and "Download" in str(link):
            filename = link.get("href")
        if "fingerprint" in str(link):
            checksum_url = link.get("href")

    #get checksum_32
    req = Request(url=checksum_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    checksum = str(page_soup).split(" ")[0]

    return checksum
#########################################################
