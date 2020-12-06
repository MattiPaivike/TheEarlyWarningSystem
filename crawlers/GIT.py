from .WebCrawlerSettings import *

#main variables
name = "Git"
url = "https://api.github.com/repos/git-for-windows/git/releases/latest"

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
    req = requests.get(url, headers=headers)
    jsoni = req.json()
    jsoni = json.dumps(jsoni)
    dict_json = json.loads(jsoni)

    return dict_json

#######################################

def crawl_version(data):

    versions_list = []

    version = data["name"]
    version = version.replace("Git for Windows ","")

    if "(" in str(version):
        version = version.replace("(",".")
        version = version.replace(")","")

    versions_list.append(version)

    return versions_list

################################################################

def crawl_dllink_x86(version, data):
    assets = data["assets"]
    #find download links
    for asset in assets:
        if "32-bit.exe" in asset["name"]:
            dllink32bit = asset["browser_download_url"]

    return dllink32bit
#########################################################
def crawl_dllink_x64(version, data):
    assets = data["assets"]
    #find download links
    for asset in assets:
        if "64-bit.exe" in asset["name"]:
            dllink64bit = asset["browser_download_url"]

    return dllink64bit
########################################################

def crawl_checksum_x86(version, data):
    #parse body for checksum data
    body = data["body"]

    r32 = "^Git-" + version + "-32-bit.exe.*"
    result32 = re.findall(r32, body, flags=re.MULTILINE)
    checksum32 = str(result32[0]).replace("Git-" + version + "-32-bit.exe | ","")

    return checksum32
#########################################################

def crawl_checksum_x64(version, data):
    #parse body for checksum data
    body = data["body"]

    r64 = "^Git-" + version + "-64-bit.exe.*"
    result64 = re.findall(r64, body, flags=re.MULTILINE)
    checksum64 = str(result64[0]).replace("Git-" + version + "-64-bit.exe | ","")

    return checksum64
#########################################################
