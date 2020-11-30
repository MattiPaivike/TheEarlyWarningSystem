from .WebCrawlerSettings import *

#main variables
name = "Jet Reports"
url = "https://support.jetglobal.com/hc/en-us/articles/223125607-Jet-Reports-Release-Notes"

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

    r = "Build (.*?)</strong>"

    strongs = data.findAll("strong")

    versions_list = re.findall(r, str(strongs))
    versions_list = [w.replace('<br/>', '') for w in versions_list]
    versions_list = [w.replace('</span>', '') for w in versions_list]

    return versions_list

################################################################
