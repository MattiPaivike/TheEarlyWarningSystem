from .WebCrawlerSettings import *

#main variables
name = "Igor Pavlov 7zip"
url = "https://www.7-zip.org/download.html"

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

    bss = data.findAll("b")

    versions_temp = []

    for b in bss:
        if "Download 7-Zip" in b.text and "for Windows" in b.text and "alpha" not in b.text and "beta" not in b.text:
            versions_temp.append(b.text)

    r = '\d*\.\d*'

    versions_list = re.findall(r, str(versions_temp))

    version = versions_list[0]

    versions_list = []
    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    links = data.findAll("a")

    main_url = "https://www.7-zip.org/"

    found_dllinks = []

    for link in links:
        if version.replace(".","") in str(link) and "msi" in str(link):
            found_dllinks.append(link.get("href"))

    for link in found_dllinks:
        if "x64" in link:
            dllink_x64 = main_url + link
        else:
            dllink_x86 = main_url + link

    return dllink_x86
#########################################################
def crawl_dllink_x64(version, data):
    links = data.findAll("a")

    main_url = "https://www.7-zip.org/"

    found_dllinks = []

    for link in links:
        if version.replace(".","") in str(link) and "msi" in str(link):
            found_dllinks.append(link.get("href"))

    for link in found_dllinks:
        if "x64" in link:
            dllink_x64 = main_url + link
        else:
            dllink_x86 = main_url + link

    return dllink_x64
########################################################
