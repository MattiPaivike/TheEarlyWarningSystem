from .WebCrawlerSettings import *

#main variables
name = "PHP (Current Stable)"
url = "https://www.php.net/downloads.php"

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

    r = '\d\.\d{1,2}\.\d{1,2}'

    divs = data.findAll("section", {"id": "layout-content"})

    for div in divs:
        h3 = div.findAll("h3")
        for span in h3:
            findspan = span.find("span")
            if findspan:
                if findspan.text == "Current Stable":
                    search = (re.search(r, str(h3)))
                    versions_list.append(search.group(0))

    return versions_list

################################################################
