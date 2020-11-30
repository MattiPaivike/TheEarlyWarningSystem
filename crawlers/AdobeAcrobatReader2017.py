from .WebCrawlerSettings import *

#main variables
name = "Adobe Acrobat Reader 2017"
url = "https://helpx.adobe.com/fi/acrobat/release-note/release-notes-acrobat-reader.html"

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
    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    repElemList = page_soup.find_all("div", class_="table parbase section")

    return repElemList

#######################################

def crawl_version(data):
    links = []

    for link in data:
        atag = link.findAll("a")
        if "classic" in str(atag):
            links.append(atag)

    r = '17.\d\d\d\.\d\d\d\d\d'

    versions_list = re.findall(r, str(links))

    return versions_list

################################################################

def crawl_dllink(version, data):
    links = []

    for link in data:
        atag = link.findAll("a")
        if "classic" in str(atag):
            links.append(atag)

    r = '17.\d\d\d\.\d\d\d\d\d'

    versions_list = re.findall(r, str(links))

    versions_str = [ str(x).replace(".","") for x in versions_list ]
    versions_str = [ int(x) for x in versions_str ]

    highest_str = max(versions_str)
    versiondata = str(highest_str).replace(".","")

    dllink = "https://ardownload2.adobe.com/pub/adobe/acrobat/win/Acrobat2017/" + versiondata + "/Acrobat2017Upd" + versiondata + ".msp"

    return dllink
#########################################################
