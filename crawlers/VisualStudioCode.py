from .WebCrawlerSettings import *

#main variables
name = "Visual Studio Code"
url = "https://code.visualstudio.com/sha"

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
    req = requests.get(url, headers=headers)

    jsoni = req.json()
    jsoni = json.dumps(jsoni)
    dict_json = json.loads(jsoni)

    return dict_json

#######################################

def crawl_version(data):

    products = data["products"]

    versions_list = []

    for product in products:
        if product["platform"]["prettyname"] == "Windows System Installer (64 bit)" and "insider" not in product["name"]:
            dllink_system_64 = product["url"]
            checksum_system_64 = product["sha256hash"]
            version = product["productVersion"]

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):

    products = data["products"]

    for product in products:
        if product["platform"]["prettyname"] == "Windows System Installer (32 bit)" and "insider" not in product["name"]:
            dllink_system_32 = product["url"]
            checksum_system_32 = product["sha256hash"]
        if product["platform"]["prettyname"] == "Windows System Installer (64 bit)" and "insider" not in product["name"]:
            dllink_system_64 = product["url"]
            checksum_system_64 = product["sha256hash"]

    return dllink_system_32
#########################################################
def crawl_dllink_x64(version, data):

    products = data["products"]

    for product in products:
        if product["platform"]["prettyname"] == "Windows System Installer (32 bit)" and "insider" not in product["name"]:
            dllink_system_32 = product["url"]
            checksum_system_32 = product["sha256hash"]
        if product["platform"]["prettyname"] == "Windows System Installer (64 bit)" and "insider" not in product["name"]:
            dllink_system_64 = product["url"]
            checksum_system_64 = product["sha256hash"]

    return dllink_system_64
########################################################

def crawl_checksum_x86(version, data):

    products = data["products"]

    for product in products:
        if product["platform"]["prettyname"] == "Windows System Installer (32 bit)" and "insider" not in product["name"]:
            dllink_system_32 = product["url"]
            checksum_system_32 = product["sha256hash"]
        if product["platform"]["prettyname"] == "Windows System Installer (64 bit)" and "insider" not in product["name"]:
            dllink_system_64 = product["url"]
            checksum_system_64 = product["sha256hash"]

    return checksum_system_32
#########################################################

def crawl_checksum_x64(version, data):

    products = data["products"]

    for product in products:
        if product["platform"]["prettyname"] == "Windows System Installer (32 bit)" and "insider" not in product["name"]:
            dllink_system_32 = product["url"]
            checksum_system_32 = product["sha256hash"]
        if product["platform"]["prettyname"] == "Windows System Installer (64 bit)" and "insider" not in product["name"]:
            dllink_system_64 = product["url"]
            checksum_system_64 = product["sha256hash"]

    return checksum_system_64
#########################################################
