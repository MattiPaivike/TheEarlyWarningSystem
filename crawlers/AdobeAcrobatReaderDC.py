from .WebCrawlerSettings import *

#main variables
name = "Adobe Acrobat Reader DC"
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
    r = '\d\d\.\d\d\d\.\d\d\d\d\d'

    for elem in data:
        if "DC," in elem.text:
            element = elem

    versions_list = re.findall(r, str(element))

    versions = [ verparse.parse(str(x)) for x in versions_list ]

    return versions_list

################################################################

def crawl_dllink(version, data):
    r = '\d\d\.\d\d\d\.\d\d\d\d\d'

    for elem in data:
        if "DC," in elem.text:
            element = elem
    versions_list = re.findall(r, str(element))

    versions = [ verparse.parse(str(x)) for x in versions_list ]
    #determine highest version
    highest = max(versions)
    #find index of highest version
    indexi = versions.index(highest)
    #use the index to find the corresponding string item for download link
    version_string = versions_list[indexi]
    #cleanup string for dllink
    version_string = version_string.replace(".","")

    dllink = "https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/" + version_string + "/AcroRdrDCUpd" + version_string + ".msp"

    return dllink
#########################################################
