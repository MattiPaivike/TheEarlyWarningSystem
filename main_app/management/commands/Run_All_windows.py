import logging
import os
import sys
from pathlib import Path

#get script directory
scriptdir = sys.path[0]
#get parent directory for manage.py and logfiles folder
mainpath = Path(str(scriptdir)).parents[2]
#get virtual enviroment folder
virtualenv = str(Path(str(scriptdir)).parents[2]) + '\\venv\scripts\python.exe'

logfilename = str(mainpath) + '/Logfiles/Run_All_logfile.log'
logging.basicConfig(filename=logfilename,level=logging.DEBUG,format = '%(asctime)s  %(levelname)-10s %(processName)s  %(name)s %(message)s')

logging.info('Starting RUNALL job')
#get all scripts in management commands folder
scripts = os.listdir(scriptdir)

#run all management commands
for script in scripts:
    if "Crawler_" in str(script):
        runscript = str(script).replace('.py', '')
        logging.info('Running script: ' + str(runscript))
        script = str(script).replace(".py", "")
        scriptpath = str(mainpath) + "\manage.py"
        scriptcommand = "\"" + virtualenv + "\"" + " " + '"' + scriptpath + '"' + " " + script
        scriptcommand = scriptcommand.replace('\\', '/')
        os.system(scriptcommand)
        print(scriptcommand)


logging.info('RUNALL Job completed. Sending email.')
scriptcommand = "\"" + virtualenv + "\"" + " " + '"' + scriptpath + '"' + " " + "email" + " Run_all '' '' '' '' '' '' ''"
scriptcommand = scriptcommand.replace('\\', '/')
os.system(scriptcommand)
