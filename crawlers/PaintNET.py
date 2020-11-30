from .WebCrawlerSettings import *

#main variables
name = "Paint.NET"
url = "https://www.getpaint.net/download.html"

##################################################
#define main settings
find_dllink = True
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = False
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = ""

New_App = False
#################################

def crawl_data(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    return page_soup

#######################################

def crawl_version(data):

    versions_list = []

    repElemList = data.findAll("table", {"id": "table8"})

    #find the strong tags
    for repElem in repElemList:
        repElemID = repElem.find('strong')
        versions_list.append(repElemID.text)

    return versions_list

################################################################

def crawl_dllink(version, data):
    url = "https://www.dotpdn.com/downloads/pdn.html"

    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    divs = page_soup.findAll("a")

    for div in divs:
        if "paint.net " in str(div) and "/files/paint.net" in str(div):
            link = div.get("href")

    #clean link
    link = link.replace("..","")

    dllink = "https://www.dotpdn.com" + link

    return dllink
########################################################
