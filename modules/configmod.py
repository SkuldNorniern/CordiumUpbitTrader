import configparser
from modules import loggermod as lgm
from time import strftime
import os.path
file_ifd = '../infodata.dat'
file_cfg = '../config.cfg'


def init():
    lgm.logmsg('Start initlizling data module','debug')
    if os.path.exists(file_ifd):
        lgm.logmsg('Infodata Detected Continue to boot.','info')
    else:
        lgm.logmsg('Generating base data file.','warn')
        init_infodata()

    if os.path.exists(file_cfg):
        lgm.logmsg('Config Detected Continue to boot.','info')
    else:
        lgm.logmsg('Generating configuration file.','warn')
        init_config()


def init_infodata():
    data = configparser.ConfigParser()
    data['info'] = {}
    data['info']['title'] = 'Cordium Upbit Trader'
    data['info']['version'] = '1.0'
    data['info']['author'] = 'Skuld Norniern'
    with open(file_ifd, 'w', encoding='utf-8') as configfile:
        data.write(configfile)


def init_config():
    cfg = configparser.ConfigParser()
    cfg['keys'] = {}
    cfg['keys']['access_key'] = 'YOUR_ACCESS_KEY'
    cfg['keys']['secret_key'] = 'YOUR_SECRET_KEY'
    cfg['keys']['server_url'] = 'https://api.upbit.com'
    cfg['system'] = {}
    cfg['system']['white_list']='BTC,ETH,XRP,ETC,OMG,ZEC,XMR,XLM,ADA,EOS,ONT,MFT,BAT,LOOM,BCH,ZIL,IOST'
    cfg['system']['growth_period']='3'
    cfg['system']['max_per_coin']='15000'
    cfg['system']['max_watchlist']='4'
    cfg['system']['term']='0.002'
    with open(file_cfg, 'w', encoding='utf-8') as configfile:
        cfg.write(configfile)


def version_read():
    data = configparser.ConfigParser()
    data.read(file_ifd, encoding='utf-8')
    title = data['info']['title']
    ver = data['info']['version']
    msg=title + ' ' + ver + ' is running.'
    lgm.logmsg(msg,'info')


def keys_read():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    ack = cfg['keys']['access_key']
    sck = cfg['keys']['secret_key']
    svu = cfg['keys']['server_url']
    return (ack,sck,svu)
