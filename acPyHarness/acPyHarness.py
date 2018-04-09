# Harness for initial development of Assetto Corsa Python apps
# Assetto Corsa uses Python 3.3
import importlib
import os
import sys
import logging
from acInTk import acUpdate, noAcUpdate

# Assetto Corsa Python app under development:
# (in this case ..\AssettoCorsa\apps\python\driftbox\driftbox.py)
appName = 'driftbox'  # the app module name is Case Sensitive, so Sidekick for example
#appName = 'admintools'
#appName = 'proTyres'
#appName = 'camber-extravaganza'
appPath = os.path.join(os.getcwd(),  'apps', 'python', appName)

# create logger
logger = logging.getLogger(appName)
logger.setLevel(logging.DEBUG)  # DEBUG INFO WARNING ERROR
# create file handler which logs even debug messages
logFileName = 'acHarness.log'
if os.path.exists(logFileName):
  os.remove(logFileName)
fh = logging.FileHandler(logFileName)
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# set a format which is simpler for console use
ch_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
ch.setFormatter(ch_formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.info('creating an instance of %s' % appName)
sys.path.append(appPath)
appModule = importlib.import_module(appName)

ac_version = '1.15.2'
deltaT = 2000 # mS interval when AC updates this app

def main():
  logger.info("Call app's acMain() as if called from AC")
  appModule.acMain(ac_version)

  logger.info("Repeatedly call app's acUpdate() as if called from AC")
  try:
    acUpdate(deltaT, appModule.acUpdate)
  except:
    logger.info("App doesn't have acUpdate()")
    noAcUpdate()

main()