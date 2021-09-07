import os
import jwt
import uuid
import json
import time
import hashlib
import pyupbit
import telegram
import pandas as pd
from pytz import timezone
from datetime import datetime
from modules import loggermod as lgm
from modules import configmod as cfm
from urllib.parse import urlencode

import requests

access_key = ''
secret_key = ''
server_url = ''

coin_list = []
upbit = ''
token = ''
mc = ''
bot = 0
df = pd.read_csv('dataset.csv')
df2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])
# 변수 설정
n = 0
percent_list = 0 # 가진 돈의 5프로씩만 투자함
INF = 0
skip_list = []
money_list = 0
op_mode = 0
hold = 0
target = 0
prices = 0
save1 = True
save2 = True
save3 = True

krw_balance = 0
now = 0
prev_day = 0
yesterday_ma15 = 0


def init_account():
    lgm.logmsg('Loading accounts data.','info')
    access_key,secret_key,server_url,token,mc = cfm.keys_read()

    if access_key =='YOUR_ACCESS_KEY':
        lgm.logmsg('Enter Your Upbit ACCESS KEY','cric')
    else :
        msg='Access key '+access_key+ ' loaded.'
        lgm.logmsg(msg,'debug')
    if secret_key =='YOUR_SECRET_KEY':
        lgm.logmsg('Enter Your Upbit SECRET KEY','cric')
    else :
        msg='Access key '+access_key+ ' loaded.'
        lgm.logmsg(msg,'debug')

    msg='Server url '+server_url+ ' loaded.'
    lgm.logmsg(msg,'debug')

    if token =='YOUR_TELEGRAM_TOKEN':
        lgm.logmsg('Enter Your telegram TOKEN','cric')
    else :
        msg='Telegram bot token '+token+ ' loaded.'
        lgm.logmsg(msg,'debug')

    if secret_key =='YOUR_TELEGRAM_MC':
        lgm.logmsg('Enter Your Telegram MC','cric')
    else :
        msg='Telegram userid '+mc+ ' loaded.'
        lgm.logmsg(msg,'debug')
        bot=telegram.Bot(token)
        bot.sendMessage(mc,'Auto Trader Online')

    lgm.logmsg('Sended message from telegram bot','info')
    pyupbit.Upbit(access_key, secret_key)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    msg='whitelist '+whl+ ' loaded.'
    lgm.logmsg(msg,'info')
    trader(access_key,secret_key,server_url,token,mc)


#def account_req():
#    payload = {
#        'access_key': access_key,
#        'nonce': str(uuid.uuid4()),
#    }
#    jwt_token = jwt.encode(payload, secret_key)
#    authorize_token = 'Bearer {}'.format(jwt_token)
#    headers = {"Authorization": authorize_token}
#    res = requests.get(server_url + "/v1/accounts", headers=headers)
#    print(res.json())
