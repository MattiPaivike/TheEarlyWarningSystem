from .WebCrawlerSettings import *

#main variables
name = "Inkscape"
url = "https://inkscape.org/release"

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

    divs = page_soup.findAll("div", {"id": "sidecategory"})

    for div in divs:
        if "Inkscape" in div.text:
            divi = div.find("h1")

    return divi

#######################################

def crawl_version(data):
    versions_list = []

    version = data.text
    version = str(version).replace("Inkscape ", "")

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    url32 = "https://inkscape.org/release/inkscape-" + version + "/windows/32-bit/msi/dl"

    req = Request(url=url32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")

    file32 = "inkscape-" + version + "-x86.msi"

    for a in links:
        if file32 in str(a) and "sha256" not in str(a):
            dllink32 = a.get("href")

    dllink32 = "https://inkscape.org" + dllink32

    return dllink32


################################################################

def crawl_checksum_x86(version, data):

    url32 = "https://inkscape.org/release/inkscape-" + version + "/windows/32-bit/msi/dl"

    req = Request(url=url32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")

    for a in links:
        if "sha256" in str(a):
            checksum32 = a.get("href")

    req = Request(url=checksum32, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    file32 = "inkscape-" + version + "-x86.msi"

    if file32 in str(page_soup):
        page_list = str(page_soup).strip()
        page_list = page_list.split(" ")
        checksum32 = page_list[0]

    return checksum32

################################################################

def crawl_dllink_x64(version, data):

    url64 = "https://inkscape.org/release/inkscape-" + version + "/windows/64-bit/msi/dl"

    req = Request(url=url64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")
    file64 = "inkscape-" + version + "-x64.msi"

    for a in links:
        if file64 in str(a) and "sha256" not in str(a):
            dllink64 = a.get("href")

    dllink64 = "https://inkscape.org" + dllink64

    return dllink64

################################################################

def crawl_checksum_x64(version, data):

    url64 = "https://inkscape.org/release/inkscape-" + version + "/windows/64-bit/msi/dl"

    req = Request(url=url64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    links = page_soup.findAll("a")

    for a in links:
        if "sha256" in str(a):
            checksum64 = a.get("href")

    req = Request(url=checksum64, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    file64 = "inkscape-" + version + "-x64.msi"

    if file64 in str(page_soup):
        page_list = str(page_soup).strip()
        page_list = page_list.split(" ")
        checksum64 = page_list[0]

    return checksum64


################################################################

#save these for later testing
#data = crawl_data(url)
#version = crawl_version(data)
#latest_versions = [ verparse.parse(str(x)) for x in version ]
#highest = max(latest_versions)
#check = crawl_checksum_x64(str(highest),data)
#check2= crawl_checksum_x86(str(highest),data)
