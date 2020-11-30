from .WebCrawlerSettings import *

#main variables
name = "RStudio"
url = "https://rstudio.com/products/rstudio/download/"

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

    divs = data.find("h3", {"id": "download"})

    r = '\d\.\d*\.\d*'

    versions_list = re.findall(r, str(divs))

    return versions_list

#########################################################
def crawl_dllink(version, data):

    bodies = data.findAll("tbody")

    for table in bodies:
        if "Windows 10" in str(table) and "exe" in str(table):
            links = table.findAll("a")

    for link in links:
        if "exe" in str(link) and "https" in str(link):
            dllink = link.get("href")
        if "SHA" in str(link):
            checksum = link.get("data-content")

    return dllink
########################################################

def crawl_checksum(version, data):

    bodies = data.findAll("tbody")

    for table in bodies:
        if "Windows 10" in str(table) and "exe" in str(table):
            links = table.findAll("a")

    for link in links:
        if "exe" in str(link) and "https" in str(link):
            dllink = link.get("href")
        if "SHA" in str(link):
            checksum = link.get("data-content")

    return checksum
#########################################################
