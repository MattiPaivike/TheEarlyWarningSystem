from .WebCrawlerSettings import *

#main variables
name = "WinSCP"
url = "https://winscp.net/eng/download.php"

##################################################
#define main settings
find_dllink = True
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = True
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = "SHA256"

New_App = False
#################################

def crawl_data(url):
    req = Request(url=url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    return page_soup

#######################################

def crawl_version(data):

    divs = data.findAll("section", {"class": "gradient-bg-reverse download-info"})
    for div in divs:
        a = div.find("a", {"class": "btn btn-primary btn-lg"})

    r = 'WinSCP-\S*-Setup.exe'

    result = re.search(r, str(a))
    result = str(result.group(0)).replace("WinSCP-", "")
    result = result.replace("-Setup.exe", "")

    versions_list = []
    versions_list.append(result)

    return versions_list

#########################################################
def crawl_dllink(version, data):

    link = data.find("a", {"class" : "btn btn-primary btn-lg"})
    link = link.get("href")
    dllink_url = "https://winscp.net" + link

    req = Request(url=dllink_url, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    link = page_soup.find("a", {"class" : "btn btn-primary btn-lg"})
    link = link.get("href")
    dllink = link

    return dllink
########################################################

def crawl_checksum(version, data):

    link = data.find("a", {"class" : "btn btn-primary btn-lg"})
    link = link.get("href")
    dllink_url = "https://winscp.net" + link

    #use readme.txt to get checksum
    checksum_link = dllink_url.replace("Setup.exe","ReadMe.txt")

    #navigate to readme.txt
    req = Request(url=checksum_link, headers=headers)
    page_html = uReq(req).read()
    page_soup = soup(page_html, "html.parser")

    #split readme.txt to lines so we can loop
    lines = str(page_soup).split("\n")

    matchses = []

    for line in lines:
        if "SHA-256" in line:
            matchses.append(line)

    #we expect to first match to be the checksum
    checksum = matchses[0]

    checksum = checksum.replace(" - SHA-256: ", "")
    checksum = checksum.strip()

    return checksum
########################################################
