from .WebCrawlerSettings import *

#main variables
name = "Microsoft Edge Chromium (Stable)"
url = "https://www.microsoft.com/en-us/edge/business/download"

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

    divs = page_soup.findAll("div", {"class": "c-download"})

    for div in divs:
        jsoni = (div['data-whole-json'])

    jsoni = json.loads(jsoni)

    return jsoni

#######################################

def crawl_version(data):
    versions_list = []

    for key in data:
        if key["Product"] == 'Stable':
            for k in key["Releases"]:
                if k["Platform"] == "Windows":
                    versions_list.append(k["ProductVersion"])

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    for key in data:
        if key["Product"] == 'Stable':
            for k in key["Releases"]:
                if k["Platform"] == "Windows" and k["ProductVersion"] == version and k["Architecture"] == "x86":
                    dllink_x86 = k["Artifacts"][0]["Location"]

    return dllink_x86


################################################################

def crawl_checksum_x86(version, data):

    for key in data:
        if key["Product"] == 'Stable':
            for k in key["Releases"]:
                if k["Platform"] == "Windows" and k["ProductVersion"] == version and k["Architecture"] == "x86":
                    checksum_x86 = k["Artifacts"][0]["Hash"]

    return checksum_x86

################################################################

def crawl_dllink_x64(version, data):

    for key in data:
        if key["Product"] == 'Stable':
            for k in key["Releases"]:
                if k["Platform"] == "Windows" and k["ProductVersion"] == version and k["Architecture"] == "x64":
                    dllink_x64 = k["Artifacts"][0]["Location"]

    return dllink_x64

################################################################

def crawl_checksum_x64(version, data):

    for key in data:
        if key["Product"] == 'Stable':
            for k in key["Releases"]:
                if k["Platform"] == "Windows" and k["ProductVersion"] == version and k["Architecture"] == "x64":
                    checksum_x64 = k["Artifacts"][0]["Hash"]

    return checksum_x64

################################################################
