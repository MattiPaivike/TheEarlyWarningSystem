from .WebCrawlerSettings import *

#main variables
name = "Python"
url = "https://www.python.org/downloads/windows/"

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

    links = data.findAll("a")

    for link in links:
        if "Latest Python 3 Release" in str(link):
            nextlink = link

    version = nextlink.text
    version = version.replace("Latest Python 3 Release - Python ","")

    versions_list.append(version)

    return versions_list

#########################################################
def crawl_dllink_x64(version, data):

    links = data.findAll("a")

    for link in links:
        if "Latest Python 3 Release" in str(link):
            nextlink = link.get("href")

    nextlink = "https://www.python.org" + str(nextlink)

    req = Request(url=nextlink, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")

    #get download link
    for link in links:
        if "Windows installer (64-bit)" in str(link):
            dllink = link.get("href")


    return dllink
########################################################

def crawl_dllink_x86(version, data):

    links = data.findAll("a")

    for link in links:
        if "Latest Python 3 Release" in str(link):
            nextlink = link.get("href")

    nextlink = "https://www.python.org" + str(nextlink)

    req = Request(url=nextlink, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")

    #get download link
    for link in links:
        if "Windows installer (32-bit)" in str(link):
            dllink = link.get("href")


    return dllink
########################################################

def crawl_checksum_x64(version, data):

    links = data.findAll("a")

    for link in links:
        if "Latest Python 3 Release" in str(link):
            nextlink = link.get("href")

    nextlink = "https://www.python.org" + str(nextlink)

    req = Request(url=nextlink, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #get checksum
    trs = page_soup.findAll("tr")
    for tr in trs:
        if "Windows installer (64-bit)" in str(tr):
            tds = tr.findAll("td")

    #we expect the third index to be the checksum in this table
    checksum = str(tds[3].text)

    return checksum
#########################################################

def crawl_checksum_x86(version, data):

    links = data.findAll("a")

    for link in links:
        if "Latest Python 3 Release" in str(link):
            nextlink = link.get("href")

    nextlink = "https://www.python.org" + str(nextlink)

    req = Request(url=nextlink, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #get checksum
    trs = page_soup.findAll("tr")
    for tr in trs:
        if "Windows installer (32-bit)" in str(tr):
            tds = tr.findAll("td")

    #we expect the third index to be the checksum in this table
    checksum = str(tds[3].text)

    return checksum
#########################################################
