from os.path import dirname, basename, isfile, join
import glob

#headers for web-crawler
headers = {'User-Agent': 'TheEarlyWarningSystemBot https://earlywarningsys.net/about_bot'}

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]
from . import *
