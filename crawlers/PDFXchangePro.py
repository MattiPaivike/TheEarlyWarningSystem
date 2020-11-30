from .WebCrawlerSettings import *

#main variables
name = "PDF-XChange Pro"
url = "https://www.tracker-software.com/product/pdf-xchange-pro"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = True
find_dllink_x64 = True

find_checksum = False
find_checksum_x86 = True
find_checksum_x64 = True

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

    version = data.find("h5", {"class" : "version"})
    version = version.text
    version = version.replace("Current version: ","").strip()

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    links = data.findAll("a")

    for link in links:
        if "64 bit MSI Installer" in str(link):
            nexturl_64 = link.get("href")
        if "32 bit MSI Installer" in str(link):
            nexturl_32 = link.get("href")

    #get 32bit link and checksum
    req = Request(url=nexturl_32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    div = page_soup.find("div", {"class": "downloadlink"})

    dllink_32 = div.find("a")
    checksum_32 = div.find("code")

    dllink_32 = dllink_32.get("href")
    dllink_32 = dllink_32.split("?")
    dllink_32 = dllink_32[0]
    checksum_32 = str(checksum_32.text)

    return dllink_32
#########################################################
def crawl_dllink_x64(version, data):
    links = data.findAll("a")

    for link in links:
        if "64 bit MSI Installer" in str(link):
            nexturl_64 = link.get("href")
        if "32 bit MSI Installer" in str(link):
            nexturl_32 = link.get("href")

    #get 32bit link and checksum
    req = Request(url=nexturl_64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    div = page_soup.find("div", {"class": "downloadlink"})

    dllink_64 = div.find("a")
    checksum_32 = div.find("code")

    dllink_64 = dllink_64.get("href")
    dllink_64 = dllink_64.split("?")
    dllink_64 = dllink_64[0]
    checksum_32 = str(checksum_32.text)

    return dllink_64
########################################################

def crawl_checksum_x86(version, data):
    links = data.findAll("a")

    for link in links:
        if "64 bit MSI Installer" in str(link):
            nexturl_64 = link.get("href")
        if "32 bit MSI Installer" in str(link):
            nexturl_32 = link.get("href")

    #get 32bit link and checksum
    req = Request(url=nexturl_32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    div = page_soup.find("div", {"class": "downloadlink"})

    dllink_32 = div.find("a")
    checksum_32 = div.find("code")

    dllink_32 = dllink_32.get("href")
    dllink_32 = dllink_32.split("?")
    dllink_32 = dllink_32[0]
    checksum_32 = str(checksum_32.text)

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):
    links = data.findAll("a")

    for link in links:
        if "64 bit MSI Installer" in str(link):
            nexturl_64 = link.get("href")
        if "32 bit MSI Installer" in str(link):
            nexturl_32 = link.get("href")

    #get 32bit link and checksum
    req = Request(url=nexturl_64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    div = page_soup.find("div", {"class": "downloadlink"})

    dllink_64 = div.find("a")
    checksum_64 = div.find("code")

    dllink_64 = dllink_64.get("href")
    dllink_64 = dllink_64.split("?")
    dllink_64 = dllink_64[0]
    checksum_64 = str(checksum_64.text)

    return checksum_64
#########################################################
