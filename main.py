
from modules import upbitmod as ubm
from modules import loggermod as lgm
from modules import configmod as cfm


lgm.init()
lgm.logmsg('Initlizing logger module finished.','debug')
cfm.init()
lgm.logmsg('Initlizling data module finished.','debug')
cfm.version_read()
ubm.init_account()
lgm.logmsg('Loading updit account data finished.','debug')
