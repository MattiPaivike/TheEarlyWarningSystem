from .WebCrawlerSettings import *

#main variables
name = "Citrix Workspace app"
url = "https://www.citrix.com/fi-fi/downloads/workspace-app/windows/workspace-app-for-windows-latest.html"

##################################################
#define main settings
find_dllink = False
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

#######################################

def crawl_version(data):

    versions_list = []

    divs = data.findAll("div", {"class":"text section"})

    for div in divs:
        if "Version:" in str(div):
            finaldiv = div

    ps = finaldiv.findAll("p")

    for p in ps:
        if "Version:" in p.text:
            final_paragraph = p.text

    final_paragraph = final_paragraph.replace("Version:","")
    final_paragraph = final_paragraph.strip()
    final_paragraph = final_paragraph.split(" ")

    version = final_paragraph[0]

    versions_list.append(version)

    return versions_list

################################################################
