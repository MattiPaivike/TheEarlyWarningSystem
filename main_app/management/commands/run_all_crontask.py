import logging
import os
import sys
from pathlib import Path

#this script is used to activate the Django management command via cron.

#get script directory
scriptdir = sys.path[0]
#get parent directory for manage.py and logfiles folder
mainpath = Path(str(scriptdir)).parents[2]
logfilename = str(mainpath) + '/Logfiles/Run_All_logfile.log'
logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

logging.info('Starting RUNALL job')


#build script command and run it
scriptpath = str(mainpath) + "\manage.py"

script = "main_runner"

scriptcommand = "/home/assayks/VersionChecker/venv/bin/python " + '"' + scriptpath + '"' + " " + script
scriptcommand = scriptcommand.replace('\\', '/')
os.system(scriptcommand)

logging.info('RUNALL Job completed.')
