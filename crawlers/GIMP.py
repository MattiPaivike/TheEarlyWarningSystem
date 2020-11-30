from .WebCrawlerSettings import *

#main variables
name = "GIMP"
url = "https://www.gimp.org/downloads"

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

    divs = data.find("html")

    versions_list = []

    r = 'The current stable release of GIMP is \S*'
    version_data = re.findall(r, str(divs))
    result = re.search('>(.*)<', str(version_data))
    versions_list.append(str(result.group(1)))

    return versions_list

################################################################

def crawl_dllink(version, data):
    dllink = data.find("a", {"id": "win-download-link"})
    dllink = dllink.get("href")
    dllink = "https:" + dllink

    return dllink
#########################################################

def crawl_checksum(version, data):
    div = data.find("div", {"id": "win"})
    ps = div.findAll("p")

    for p in ps:
        if "The SHA256 hash sum for" in str(p):
            checksum = p.find("kbd")

    checksum = checksum.text

    return checksum
#########################################################
