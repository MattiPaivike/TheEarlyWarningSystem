from .WebCrawlerSettings import *

#main variables
name = "Greenshot"
url = "https://api.github.com/repos/greenshot/greenshot/releases/latest"

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
    req = requests.get(url, headers=headers)
    jsoni = req.json()
    jsoni = json.dumps(jsoni)
    dict_json = json.loads(jsoni)

    return dict_json

#######################################

def crawl_version(data):

    versions_list = []

    version = data["tag_name"]
    version = version.replace("Greenshot-RELEASE-","")

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink(version, data):
    assets = data["assets"]

    #find download links
    for asset in assets:
        if "INSTALLER-" + version + "-RELEASE.exe" in asset["name"]:
            dllink = asset["browser_download_url"]

    return dllink
#########################################################
