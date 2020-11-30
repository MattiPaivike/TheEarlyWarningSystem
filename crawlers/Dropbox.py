from .WebCrawlerSettings import *

#main variables
name = "Dropbox"
url = "https://www.dropboxforum.com/t5/Desktop-client-builds/bd-p/101003016"

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

#######################################

def crawl_version(data):

    versions_list = []

    templist = []

    divs = data.findAll("a")
    for a in divs:
        templist.append(str(a.text))

    r = 'Stable Build \S*'
    versions_list = re.findall(r, str(templist))

    #clean some unwanted strings from our list
    versions_list = [w.replace('Stable Build ', '') for w in versions_list]
    versions_list = [w.replace('\',', '') for w in versions_list]

    return versions_list

################################################################

def crawl_dllink(version, data):
    url = "https://www.dropbox.com/download?full=1&plat=win"

    req = requests.head(url, headers=headers, allow_redirects=True)

    dllink = req.url

    return dllink
#########################################################
