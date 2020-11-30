from .WebCrawlerSettings import *

#main variables
name = "Putty"
url = "https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html"

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

    r = '\d\.\d{1,2}'

    repElemList = data.find("h1")

    versions_list = re.findall(r, str(repElemList))

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    divs = data.findAll("div", {"class": "downloadrow"})

    for div in divs:
        if "32-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div32 = div
        if "64-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div64 = div

    div = temp_div32.find("a")
    dllink_32 = div.get("href")

    return dllink_32
#########################################################
def crawl_dllink_x64(version, data):
    divs = data.findAll("div", {"class": "downloadrow"})

    for div in divs:
        if "32-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div32 = div
        if "64-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div64 = div

    div = temp_div64.find("a")
    dllink_64 = div.get("href")

    return dllink_64
########################################################

def crawl_checksum_x86(version, data):

    divs = data.findAll("div", {"class": "downloadrow"})

    for div in divs:
        if "32-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div32 = div
        if "64-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div64 = div

    div = temp_div32.find("a")
    dllink_32 = div.get("href")


    checksums_url = "https://the.earth.li/~sgtatham/putty/" + version + "/sha256sums"

    req = Request(url=checksums_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #get checksum 32bit
    #parse dllink for filename
    list = dllink_32.split("/")
    #get last item in list witch is the filename
    filename32 = list.pop()

    #split page soup by lines
    lines = str(page_soup).split("\n")

    for line in lines:
        if filename32 in str(line):
            checksum_32 = line.split(" ")

    checksum_32 = checksum_32[0]

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):

    divs = data.findAll("div", {"class": "downloadrow"})

    for div in divs:
        if "32-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div32 = div
        if "64-bit" in str(div):
            if "installer.msi" in str(div) and "arm" not in str(div):
                temp_div64 = div

    div = temp_div64.find("a")
    dllink_64 = div.get("href")

    checksums_url = "https://the.earth.li/~sgtatham/putty/" + version + "/sha256sums"

    req = Request(url=checksums_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #get checksum 64bit
    #parse dllink for filename
    list = dllink_64.split("/")
    #get last item in list witch is the filename
    filename64 = list.pop()

    #split page soup by lines
    lines = str(page_soup).split("\n")

    for line in lines:
        if filename64 in str(line):
            checksum_64 = line.split(" ")

    checksum_64 = checksum_64[0]

    return checksum_64
#########################################################
