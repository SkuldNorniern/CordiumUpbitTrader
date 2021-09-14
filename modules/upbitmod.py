import os
import jwt
import uuid
import json
import time
import hashlib
import pyupbit
import telegram
import datetime
from modules import loggermod as lgm
from modules import configmod as cfm
from modules import datasetmod as dsm
import requests

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

def trader():
    def check_account():
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

    def get_amount(ticker):
        balances = upbit.get_balances()
        for b in balances:
            if b['currency'] == ticker:
                if b['balance'] is not None:
                    return (float(b['balance'])*float(b['avg_buy_price']),float(b['avg_buy_price']))
                else:
                    return (0,0)
        return (0,0)

    #dfc = pd.read_csv('dataset.csv')
    #dfc2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])
    check_account()
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    upbit=pyupbit.Upbit(access_key,secret_key)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    n = len(coin_list)
    coins=whl.split(',')
    msg='whitelist '+whl+ ' loaded.'
    lgm.logmsg(msg,'info')

    bot=telegram.Bot(token)
    buy_percent,max_per_coin,max_watchlist,real_trade=cfm.system_read()
    if real_trade=='True' : real_trade=True
    else : real_trade=False
    buy_percent=float(buy_percent)
    max_per_coin=int(max_per_coin)
    max_watchlist=int(max_watchlist)
    lgm.logmsg('Loaded System data.','info')
    for i in range(n):
        coin_list[i]='KRW-'+coin_list[i]
        coin_list[i]=str(coin_list[i])
        coins[i]=str(coins[i])
    tt=True
    while True:
        try:
            now = datetime.datetime.now()
            if (now.hour % 3) == 0 and tt==False and now.minute==0:
                tt=True
                msg = f"지금 {now.hour}시입니다. 코드가 잘 실행되고 있습니다."
                lgm.logmsg(msg,'info')
                bot.sendMessage(mc,msg)
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
                amount,avg = get_amount(coins[i])
                coin = get_balance(coins[i])
                if ma15 / ma60 >= 1.0 and ma15 / ma60 <= 1.005 and ma15_pre < ma15 and ma15_pre < ma60:
                    monyy=krw*buy_percent
                    if (krw*buy_percent) > 5500 and monyy<max_per_coin-amount and dsm.watching_list()<max_watchlist:
                            if monyy > max_per_coin:
                                monyy=max_per_coin
                            msg="%s 의 15일 이동평균선이 60일 이동평균선을 넘어섰으므로 %d 원을 매수 합니다."%(coins[i],monyy)
                            lgm.logmsg(msg,'info')
                            bot.sendMessage(mc,msg)
                            if real_trade==True:  upbit.buy_market_order(coin_list[i], krw*buy_percent)
                            dsm.report_update(now,coins[i],"buy",monyy,"N/A",krw-monyy)
                    elif monyy>max_per_coin-amount:
                        msg="%s 가 이미 %d 원 만큼 매수되어있어 매수하지 않습니다."%(coins[i],amount)
                        lgm.logmsg(msg,'info')
                        bot.sendMessage(mc,msg)
                    elif  dsm.watching_list()>max_watchlist:
                        msg="설정한 동시 거래수 %d 개에 도달해 더이상 구매하지 않습니다."%(max_watchlist)
                        lgm.logmsg("msg,"'info')
                        bot.sendMessage(mc,msg)
                    else:
                        lgm.logmsg("돈이 부족합니다.",'info')

                else:
                    if ma15 / ma15_pre < 0.99975 and ma15 / ma60 >= 1.005 and coin>0:
                        msg="%s 의 15일 이동평균선이 하락하여 매도합니다."%(coins[i])
                        lgm.logmsg(msg,'info')
                        bot.sendMessage(mc,msg)
                        dsm.report_update(now,coins[i],"sell",round(coin),round(avg),current_price)
                        upbit.sell_market_order(coin_list[i], coin)

                msg="보유 %s : %f  %s/ 보유 원화 : %d 원 / 골든크로스 비율 : %f / 이전 15일 이동평균선과 가격차이 : %d 원 / 이전 15일 이동평균선과 변화비율 : %f"%(coins[i] ,float(coin),coins[i],int(krw),float( ma15 / ma60), int(ma15 - ma15_pre), float( ma15 / ma15_pre))
                lgm.logmsg(msg,'info')
                if(tt==True): bot.sendMessage(mc,msg)
                if amount>0: dsm.data_update(coins[i],round(amount),round(coin))
                time.sleep(1)
            tt=False
            time.sleep(45)

        except Exception as e:
            lgm.logmsg(e,'err')
            time.sleep(15)
