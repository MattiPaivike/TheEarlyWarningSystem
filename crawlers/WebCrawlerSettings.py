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
import time
from datetime import datetime

#headers for web-crawler
headers = {'User-Agent': 'TheEarlyWarningSystemBot https://earlywarningsys.net/about_bot'}
