from .WebCrawlerSettings import *

#main variables
name = "Winrar"
url = "https://www.win-rar.com/download.html"

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

    r = '[5-9]\.\d*'

    repElemList = data.find("a", {"class": "download-link"})

    versions_list = re.findall(r, str(repElemList))

    return versions_list

#########################################################
def crawl_dllink_x64(version, data):

    links = data.findAll("a")

    temp_links_64 = []

    for link in links:
        if "WinRAR" in str(link) and "English" in str(link) and "64 bit" in str(link):
            temp_links_64.append(link.get("href"))

    #select first item in list because multiple identical links will be found
    nextlink64 = temp_links_64[0]

    #64 bit download links
    #navigate to next page
    req = Request(url=nextlink64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    link = page_soup.find("a",{"class":"downloadlink"})

    link = link.get("href")
    link = "https://www.win-rar.com" + link

    req = Request(url=link, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    link = page_soup.find("a",{"class":"postdownloadlink"})

    link = link.get("href")
    dllink_64 = "https://www.win-rar.com" + link

    return dllink_64
########################################################

def crawl_dllink_x86(version, data):

    links = data.findAll("a")

    temp_links_32 = []

    for link in links:
        if "WinRAR" in str(link) and "English" in str(link) and "32 bit" in str(link):
            temp_links_32.append(link.get("href"))

    #select first item in list because multiple identical links will be found
    nextlink32 = temp_links_32[0]

    #32 bit download links
    #navigate to next page
    req = Request(url=nextlink32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    link = page_soup.find("a",{"class":"downloadlink"})

    link = link.get("href")
    link = "https://www.win-rar.com" + link

    #navigate to final page
    req = Request(url=link, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    link = page_soup.find("a",{"class":"postdownloadlink"})

    link = link.get("href")
    dllink_32 = "https://www.win-rar.com" + link


    return dllink_32
