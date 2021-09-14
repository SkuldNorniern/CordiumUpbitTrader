from modules import upbitmod as ubm
from modules import loggermod as lgm
from modules import configmod as cfm
from modules import datasetmod as dsm
lgm.init()
lgm.logmsg('Initialing logger module finished.','info')
cfm.init()
lgm.logmsg('Initialing config module finished.','info')
dsm.init()
lgm.logmsg('Initialing data module finished.','info')
cfm.version_read()
lgm.logmsg('Loading account data finished.','info')
ubm.trader()
