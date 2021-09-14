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
import datetime
from modules import loggermod as lgm
from modules import configmod as cfm
from urllib.parse import urlencode
import requests



def trader():
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
        n = len(coin_list)
        coins=coin_list

        msg='whitelist '+whl+ ' loaded.'
        lgm.logmsg(msg,'info')
        sysdt = cfm.system_read()
        buy_percent=sysdt;
        lgm.logmsg('Loaded buying percent','info')
        #trader(access_key,secret_key,server_url,token,mc)

    def get_target_price(ticker, k):
        df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
        target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
        return target_price

    def get_current_price(ticker):
        return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]
    def get_start_time(ticker):
        df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
        start_time = df.index[0]
        return start_time

    def get_ma7_pre(ticker):
        pre = datetime.datetime.now() - datetime.timedelta(minutes=5)
        df = pyupbit.get_ohlcv(ticker, interval="minute5", count=15, to= pre)
        ma15 = df['close'].rolling(7).mean().iloc[-1]
        return ma15

    def get_ma7(ticker):
        df = pyupbit.get_ohlcv(ticker, interval="minute5", count=15)
        ma15 = df['close'].rolling(7).mean().iloc[-1]
        return ma15

    def get_ma15(ticker):
        df = pyupbit.get_ohlcv(ticker, interval="minute5", count=15)
        ma15 = df['close'].rolling(15).mean().iloc[-1]
        return ma15

    def get_ma15_pre(ticker):
        pre = datetime.datetime.now() - datetime.timedelta(minutes=5)
        df = pyupbit.get_ohlcv(ticker, interval="minute5", count=15, to= pre)
        ma15 = df['close'].rolling(15).mean().iloc[-1]
        return ma15

    def get_ma60(ticker):
        df = pyupbit.get_ohlcv(ticker, interval="minute5", count=60)
        ma15 = df['close'].rolling(60).mean().iloc[-1]
        return ma15

    def get_balance(ticker):
        balances = upbit.get_balances()
        for b in balances:
            if b['currency'] == ticker:
                if b['balance'] is not None:
                    return float(b['balance'])
                else:
                    return 0
        return 0

    access_key = ''
    secret_key = ''
    server_url = ''
    buy_percent=0
    coin_list = []
    coins=[]
    upbit = ''
    token = ''
    mc = ''
    bot = 0
    #dfc = pd.read_csv('dataset.csv')
    #dfc2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])
    init_account()
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    upbit=pyupbit.Upbit(access_key,secret_key)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    n = len(coin_list)
    coins=whl.split(',')
    bot=telegram.Bot(token)
    sysdt = cfm.system_read()
    buy_percent=float(sysdt);
    for i in range(n):
        coin_list[i]='KRW-'+coin_list[i]
        coin_list[i]=str(coin_list[i])
        coins[i]=str(coins[i])
    tt=False
    ts=False
    while True:
        try:
            now = datetime.datetime.now()
            if (now.hour % 3) == 0 and tt==False:
                tt=True
                msg = f"지금 {now.hour}시입니다. 코드가 잘 실행되고 있습니다."
                lgm.logmsg(msg,'info')
                bot.sendMessage(mc,msg)
            if ((now.hour % 3)+1) == now.hour and tt==True:
                tt=False
            if((now.minute%30==0)):
                ts=True
            else : ts=False
            krw = get_balance('KRW')
            msg='Balance Loaded : %d'%(krw)
            lgm.logmsg(msg,'info')
            for i in range(n):
                start_time = get_start_time(coin_list[i])
                end_time = start_time + datetime.timedelta(days=1)
                ma15 = get_ma15(coin_list[i])
                ma15_pre = get_ma15_pre(coin_list[i])
                ma60 = get_ma60(coin_list[i])
                current_price = get_current_price(coin_list[i])
                if ma15 / ma60 >= 1.0 and ma15 / ma60 <= 1.005 and ma15_pre < ma15 and ma15_pre < ma60:
                    if krw > 5500:
                            msg="%s 의 15일 이동평균선이 60일 이동평균선을 넘어섰으므로 매수 합니다."%(coins[i])
                            lgm.logmsg(msg,'info')
                            bot.sendMessage(mc,msg)
                #            upbit.buy_market_order(coin_list[i], krw*buy_percent)
                    else:
                        print("돈이 부족합니다.")

                else:
                    coin = get_balance(coins[i])
                    if ma15 / ma15_pre < 0.99975 and ma15 / ma60 >= 1.005:
                        msg="%s 의 15일 이동평균선이 하락하여 매도합니다."%(coins[i])
                        lgm.logmsg(msg,'info')
                        bot.sendMessage(mc,msg)
                        upbit.sell_market_order(coin_list[i], coin) # 테스트 중

                msg="보유 %s : %f  %s/ 보유 원화 : %d 원 / 골든크로스 비율 : %f / 이전 15일 이동평균선과 가격차이 : %d 원 / 이전 15일 이동평균선과 변화비율 : %f"%(coins[i] ,float(coin),coins[i],int(krw),float( ma15 / ma60), int(ma15 - ma15_pre), float( ma15 / ma15_pre))
                lgm.logmsg(msg,'info')
                if(ts==True): bot.sendMessage(mc,msg)
                time.sleep(2)
            time.sleep(30)

        except Exception as e:
            lgm.logmsg(e,'err')
            time.sleep(30)
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
