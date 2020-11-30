from .WebCrawlerSettings import *

#main variables
name = "Adobe Acrobat Reader 2015"
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

    return page_soup

def crawl_version(data):

    versions_list = []

    r = '\d\d\.\d\d\d\.\d\d\d\d\d'

    repElemList = data.findAll("div", class_="table parbase section")

    for elem in repElemList:
        if "DC Classic" in elem.text:
            element = elem

    versions_list = re.findall(r, str(element))

    return versions_list

def crawl_dllink(version,data):

    versiondata = str(version)
    versiondata = versiondata.split(".", maxsplit=1)
    versiondata = versiondata[0] + "00" + versiondata[1]
    versiondata = versiondata.replace(".","")

    dllink = "https://ardownload2.adobe.com/pub/adobe/acrobat/win/Acrobat2015/" + versiondata + "/Acrobat2015Upd" + versiondata + ".msp"

    return dllink
