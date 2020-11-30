from .WebCrawlerSettings import *

#main variables
name = "FileZilla"
url = "https://filezilla-project.org/download.php?show_all=1"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = True
find_dllink_x64 = True

find_checksum = False
find_checksum_x86 = True
find_checksum_x64 = True

checksum_type = "SHA512"

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

    repElemList = data.find("html")

    r = 'The latest stable version of FileZilla Client is \S*'

    result = re.search(r, str(repElemList))

    version_text = (str(result.group(0)))

    version_text = version_text.replace("</p>", "")
    version_text = version_text.replace("The latest stable version of FileZilla Client is ", "")

    versions_list.append(version_text)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    dllink_x86 = "https://download.filezilla-project.org/client/" + "FileZilla_" + version + "_win32-setup.exe"

    return dllink_x86
#########################################################
def crawl_dllink_x64(version, data):
    dllink_x64 = "https://download.filezilla-project.org/client/" + "FileZilla_" + version + "_win64-setup.exe"

    return dllink_x64
########################################################

def crawl_checksum_x86(version, data):
    divs = data.findAll("div", {"class":"downloadplatform"})

    for div in divs:
        if "Windows (32bit)" in str(div):
            checksum_x86_div = div.find("div", {"class":"details"})

    for para in checksum_x86_div:
        if "SHA" in str(para):
            checksum_x86 = para.text

    checksum_x86 = checksum_x86.replace("SHA-512 hash: ","")
    checksum_x86 = checksum_x86.strip()


    return checksum_x86
#########################################################

def crawl_checksum_x64(version, data):
    divs = data.findAll("div", {"class":"downloadplatform"})

    for div in divs:
        if "Windows (64bit)" in str(div):
            checksum_x64_div = div.find("div", {"class":"details"})

    for para in checksum_x64_div:
        if "SHA" in str(para):
            checksum_x64 = para.text

    checksum_x64 = checksum_x64.replace("SHA-512 hash: ","")
    checksum_x64 = checksum_x64.strip()

    return checksum_x64
#########################################################
