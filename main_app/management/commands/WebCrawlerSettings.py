from main_app.models import Software, Version
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

from bs4 import BeautifulSoup as soup
import urllib.request
from urllib.request import urlopen as uReq
from urllib.request import Request
from packaging import version as verparse
import re
import logging
import sys
import ssl
import requests
import json
import os
import platform
from datetime import datetime

#script directory
scriptdir = sys.path[0]

#logfile directory
logfiledir = str(scriptdir) + "/Logfiles/"

#headers for web-crawler
headers = {'User-Agent': 'TheEarlyWarningSystemBot https://earlywarningsys.net/about_bot'}
