import configparser
from modules import loggermod as lgm
#from modules import datasetmod as dsm
from time import strftime
import os.path
file_ifd = 'infodata.dat'
file_cfg = 'config.cfg'

def init():
    lgm.logmsg('Start Initialing config module','debug')
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
    cfg['keys']['telegram_token'] = 'YOUR_TELEGRAM_TOKEN'
    cfg['keys']['telegram_mc'] = 'YOUR_TELEGRAM_MC'
    cfg['system'] = {}
    cfg['system']['whitelist']='BTC,ETH,XRP,ETC,XLM,ADA,BCH,GAS'
    cfg['system']['real_trade']='False'
    cfg['system']['buy_percent']='0.1'
    cfg['system']['max_per_coin']='15000'
    cfg['system']['max_watchlist']='4'
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
    tgt = cfg['keys']['telegram_token']
    tgm = cfg['keys']['telegram_mc']
    return (ack,sck,svu,tgt,tgm)

def system_read():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    buyp = cfg['system']['buy_percent']
    mpc = cfg['system']['max_per_coin']
    mxw = cfg['system']['max_watchlist']
    rlt= cfg['system']['real_trade']
    return (buyp,mpc,mxw,rlt)

def whitelist_read():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    whl = cfg['system']['whitelist']
    return whl
