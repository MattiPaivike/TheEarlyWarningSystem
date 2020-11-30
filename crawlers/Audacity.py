from .WebCrawlerSettings import *

#main variables
name = "Audacity"
url = "https://api.github.com/repos/audacity/audacity/releases/latest"

##################################################
#define main settings
find_dllink = False
find_dllink_x86 = False
find_dllink_x64 = False

find_checksum = False
find_checksum_x86 = False
find_checksum_x64 = False

checksum_type = ""
#################################

def crawl_data(url):
    req = requests.get(url, headers=headers)

    return req

#######################################

def crawl_version(data):

    versions_list = []

    jsoni = data.json()
    jsoni = json.dumps(jsoni)
    dict_json = json.loads(jsoni)

    version = dict_json["tag_name"]
    version = version.replace("Audacity-","")

    versions_list.append(version)

    return versions_list

#########################################
