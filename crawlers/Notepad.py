from .WebCrawlerSettings import *

#main variables
name = "Notepad++"
url = "https://api.github.com/repos/notepad-plus-plus/notepad-plus-plus/releases/latest"

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

    versions_list = []

    version = data["tag_name"]
    version = version.replace("v","")

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    assets = data["assets"]

    for asset in assets:
        if "npp." + version + ".Installer.exe" in asset["name"] and "sig" not in asset["name"]:
            dllink_32 = asset["browser_download_url"]


    return dllink_32
#########################################################
def crawl_dllink_x64(version, data):
    assets = data["assets"]

    for asset in assets:
        if "npp." + version + ".Installer.x64.exe" in asset["name"] and "sig" not in asset["name"]:
            dllink_64 = asset["browser_download_url"]

    return dllink_64
########################################################

def crawl_checksum_x86(version, data):
    body = data["body"]
    body = str(body).split("\n")

    for line in body:
        if "npp." + version + ".Installer.exe" in line:
            checksum_32 = line.split(" ")
            checksum_32 = checksum_32[0]
            checksum_32 = checksum_32.strip()

    return checksum_32
#########################################################

def crawl_checksum_x64(version, data):
    body = data["body"]
    body = str(body).split("\n")

    for line in body:
        if "npp." + version + ".Installer.x64.exe" in line:
            checksum_64 = line.split(" ")
            checksum_64 = checksum_64[0]
            checksum_64 = checksum_64.strip()

    return checksum_64
#########################################################
