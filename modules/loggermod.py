import logging
logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',filename='../latest.log',filemode='w',datefmt='%m/%d/%Y %I:%M:%S', level=logging.DEBUG)

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def init():
    logmsg('Initlizing logger module.','debug')

def logmsg(msg, uglvl):
    if uglvl == 'debug':
        logging.debug(msg)
    elif uglvl == 'info':
        logging.info(msg)
    elif uglvl == 'warn':
        logging.warning(msg)
    elif uglvl == 'err':
        logging.error(msg)
    elif uglvl == 'cric':
        logging.critical(msg)
