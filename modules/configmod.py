import configparser
from modules import loggermod as lgm
from modules import datasetmod as dsm
from time import strftime
import os.path
file_ifd = 'infodata.dat'
file_cfg = 'config.cfg'
file_sdv = 'saved_data.csv'

def init():
    lgm.logmsg('Start Initialing data module','debug')
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
    if os.path.exists(file_sdv):
        lgm.logmsg('saved_data Detected Continue to boot.','info')
    else:
        lgm.logmsg('Generating save_data file.','warn')
        dsm.init_savedata()

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
    cfg['system']['whitelist']='BTC,ETH,XRP,ETC,XLM,ADA,EOS,BCH,GAS,FLOW,ETC,ZIL'
    cfg['system']['whitelist_is_updated']='1'
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
    tgt = cfg['keys']['telegram_token']
    tgm = cfg['keys']['telegram_mc']
    return (ack,sck,svu,tgt,tgm)


def whitelist_read():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    whl = cfg['system']['whitelist']
    return whl

def isupdated_read():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    wiu = cfg['system']['whitelist_is_updated']
    return wiu

def isupdated_write():
    cfg = configparser.ConfigParser()
    cfg.read(file_cfg, encoding='utf-8')
    cfg.set('system','whitelist_is_updated','0')
    with open(file_cfg, 'w', encoding='utf-8') as configfile:
        cfg.write(configfile)
