from .WebCrawlerSettings import *

#main variables
name = "Google Chrome"
url = "https://omahaproxy.appspot.com/all.json"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = True
find_dllink_x64 = True

find_checksum = False
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = ""

New_App = False
#################################

def crawl_data(url):
    response = requests.get(url)
    jsoni = response.json()

    return jsoni

#######################################

def crawl_version(data):

    versions_list = []

    version = data[0]['versions'][4]['version']
    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    dllink32bit = 'https://dl.google.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise.msi'

    return dllink32bit
#########################################################
def crawl_dllink_x64(version, data):
    dllink64bit = 'https://dl.google.com/edgedl/chrome/install/GoogleChromeStandaloneEnterprise64.msi'

    return dllink64bit
########################################################
