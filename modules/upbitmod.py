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



def cal_target(ticker):
    # time.sleep(0.1)
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    bot=telegram.Bot(token)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    df_cal_target = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df_cal_target.iloc[-2]
    today = df_cal_target.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5
    return target

def sell(ticker):
    # time.sleep(0.1)
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    bot=telegram.Bot(token)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    balance = upbit.get_balance(ticker)
    s = upbit.sell_market_order(ticker, balance)
    msg = str(ticker)+"매도 시도"+"\n"+json.dumps(s, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)
def buy(ticker, money):
    # time.sleep(0.1)
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    bot=telegram.Bot(token)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    b = upbit.buy_market_order(ticker, money)
    try:
        if b['error']:
            b = upbit.buy_market_order(ticker, 100000)
            msg = "돈 좀 부족해서 " + str(ticker)+" "+str(100000)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    except:
        msg = str(ticker)+" "+str(money)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)

def printall():
    #msg = f"------------------------------{now.strftime('%Y-%m-%d %H:%M:%S')}------------------------------\n"
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    msg="lol"
    n=len(coin_list)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    for i in range(n):
        msg += f"{'%10s'%coin_list[i]} 목표가: {'%11.1f'%target[i]} 현재가: {'%11.1f'%prices[i]} 매수금액: {'%7d'%money_list[i]} hold: {'%5s'%hold[i]} status: {op_mode[i]}\n"
    lgm.logmsg(msg,'info')

def save_data(krw_balance): # 만약 존버했을 경우와 비교를 하는 함수
    # 자신이 존버를 할 거라고 생각을 하고 해당 코인을 얼마나 가지고 있을 예정인지 변수 설정
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    bot=telegram.Bot(token)
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    own_coin_list_04_08 = [
        0, # BTC 만약 자신이 존버를 할 경우 가지고 있을 법한 비트코인 개수
        0, # ETH
        0 # DOGE
    ]
    df_saved_data = pd.read_csv('saved_data.csv')
    now_prices = [-1]*(n)
    jonbeo = "----------들고만 있었으면----------\n"
    total_jonbeo = 0
    auto_upbit = "----------자동화----------\n"
    auto_upbit += "자동화 총 금액 -> " + str(krw_balance) + "\n"
    for i in range(n):
        now_prices[i] = pyupbit.get_current_price(coin_list[i])
        total_jonbeo += now_prices[i]*own_coin_list_04_08[i]
        jonbeo += coin_list[i] + " 현 가격: " + str(now_prices[i]) + "이 코인의 총 가격" + str(now_prices[i]*own_coin_list_04_08[i]) + "\n"
        time.sleep(0.1)
    jonbeo += "지금까지 존버했으면 총 금액 -> " + str(total_jonbeo) + "\n"
    msg = jonbeo + auto_upbit + "존버와의 금액 차이 -> " + str(krw_balance - total_jonbeo) + "원 벌었음(-이면 잃은거)\n"
    try:
        dif_yesterday = krw_balance - df_saved_data.iloc[-1]['auto_upbit']
        msg += "!!어제와의 금액 차이!!: " + str(dif_yesterday)
        df2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit','difference_yesterday'])
        df2 = df2.append({'date':now.strftime('%Y-%m-%d %H:%M:%S'), 'jonbeo':total_jonbeo, 'auto_upbit': krw_balance, 'difference_jonbeo_autoupbit':krw_balance - total_jonbeo,'difference_yesterday':dif_yesterday}, ignore_index=True)
        df2.to_csv('saved_data.csv', mode='a', header=False)
    except:
        df2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])
        df2 = df2.append({'date':now.strftime('%Y-%m-%d %H:%M:%S'), 'jonbeo':total_jonbeo, 'auto_upbit': krw_balance, 'difference_jonbeo_autoupbit':krw_balance - total_jonbeo}, ignore_index=True)
        df2.to_csv('saved_data.csv', mode='a', header=False)
    print(msg)
    bot.sendMessage(mc,msg)

def get_yesterday_ma15(ticker):
    access_key,secret_key,server_url,token,mc = cfm.keys_read()
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    df_get_yesterday_ma15 = pyupbit.get_ohlcv(ticker)
    close = df_get_yesterday_ma15['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]




def trader(access_key,secret_key,server_url,token,mc):
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    n=len(coin_list)
    for i in range(n):
        coin_list[i]='KRW-'+coin_list[i]
    percent_list = [0.10]*n
    INF = 1000000000000
    money_list = [0]*(n)
    op_mode = [False] * (n) # 당일 9시에 코드를 시작하지 않았을 경우를 위한 변수
    hold = [False] * (n) # 해당 코인을 가지고 있는지
    target = [INF]*(n)
    prices = [-1]*(n)
    save1 = True
    save2 = True
    save3 = True
    krw_balance = 0
    now = datetime.now(timezone('Asia/Seoul'))
    prev_day = now.day
    yesterday_ma15 = [0]*(n)
    time_save = True
    bot=telegram.Bot(token)
    upbit = pyupbit.Upbit(access_key, secret_key)

    for i in range(n):
        target[i] = df.loc[i,'target']
        money_list[i] = df.loc[i,'money_list']
        hold[i] = df.loc[i,'hold']
        op_mode[i] = df.loc[i,'op_mode']
        yesterday_ma15[i] = df.loc[i,'yesterday_ma15']
        if coin_list[i] in skip_list:
            op_mode[i] = False
            df.loc[i,'op_mode'] = False
            df.to_csv('dataset.csv', index=None)

    while True:
        try:
            # 지금 한국 시간
            now = datetime.now(timezone('Asia/Seoul'))
            if not time_save:
                if (now.hour-1)%3 == 0:
                    time_save = True
            # 하루에 한번 작동하는 save
            if prev_day != now.day:
                prev_day = now.day
                save1 = True
                save2 = True
                save3 = True
                msg = "save 변수가 True로 업데이트 됐습니다.\nsave1: " + str(save1) + " save2 -> " + str(save2) + " save3 -> " + str(save3)
                bot.sendMessage(mc,msg)
            # 8시 50분에 코드가 실행 중인지 확인
            if now.hour == 8 and now.minute == 50 and save3:
                msg = "코드가 정상 실행 중입니다."
                bot.sendMessage(mc,msg)
                save3 = False

            # 매도 시도
            if now.hour == 8 and now.minute == 59 and save1:
                time.sleep(1)
                for i in range(n):
                    if hold[i] and op_mode[i]:
                        sell(coin_list[i])
                        hold[i] = False
                        df.loc[i, 'hold'] = False
                        op_mode[i] = False
                        df.loc[i, 'op_mode'] = False
                        df.to_csv('dataset.csv', index=None)
                print('----------전부 매도 완료----------')

                # 매도가 다 되고 나서
                time.sleep(0.1)
                krw_balance = upbit.get_balance("KRW")
                for i in range(n):
                    money_list[i] = int(krw_balance * percent_list[i])
                    df.loc[i, 'money_list'] = money_list[i]
                    df.to_csv('dataset.csv', index=None)
                msg = "----------매수할 돈 정보 갱신(money_list)----------\n"
                for i in range(n):
                    msg += coin_list[i] + " " + str(money_list[i])+"원"+"\n"
                print(msg)
                bot.sendMessage(mc,msg)
                save_data(krw_balance)
                save1 = False
                now = datetime.now(timezone('Asia/Seoul'))

            # 09:00:00 목표가 갱신
            if now.hour == 9 and now.minute == 0 and now.second > 30 and save2:
                for i in range(n):
                    target[i] = cal_target(coin_list[i])
                    op_mode[i] = True
                    df.loc[i, 'target'] = target[i]
                    df.loc[i, 'op_mode'] = True
                    df.to_csv('dataset.csv', index=None)
                    if coin_list[i] in skip_list:
                        op_mode[i] = False
                        df.loc[i, 'op_mode'] = False
                        df.to_csv('dataset.csv', index=None)
                msg = "----------목표가 갱신(target)----------\n"
                for i in range(n):
                    msg += coin_list[i] + " " + str(target[i])+"원\n"
                print(msg)
                bot.sendMessage(mc,msg)
                msg = "어제 ma15 가격 갱신\n"
                for i in range(n):
                    time.sleep(0.1)
                    yesterday_ma15[i] = get_yesterday_ma15(coin_list[i])
                    df.loc[i, 'yesterday_ma15'] = yesterday_ma15[i]
                    df.to_csv('dataset.csv', index=None)
                    msg += '%8s'%coin_list[i] + " -> " + '%11.1f'%yesterday_ma15[i] + "원\n"
                for i in range(n):
                    if yesterday_ma15[i] > target[i]:
                        msg += str(coin_list[i]) + "는 yesterday_ma15가 target보다 커서 안 사질 수도 있음 yesterday_ma15 -> " + str(yesterday_ma15[i]) + " target -> " + str(target[i]) + "\n"
                bot.sendMessage(mc,msg)
                print(msg)
                save2 = False

            # 현 가격 가져오기
            for i in range(n):
                time.sleep(0.1) # 실행할 때 주석처리
                prices[i] = pyupbit.get_current_price(coin_list[i])

            # 매초마다 조건을 확인한 후 매수 시도
            for i in range(n):
                if op_mode[i] and not hold[i] and prices[i] >= target[i] and prices[i] >= yesterday_ma15[i]:
                    # 매수
                    buy(coin_list[i], money_list[i])
                    hold[i] = True
                    df.loc[i, 'hold'] = True
                    df.to_csv('dataset.csv', index=None)
                    print('----------매수 완료------------')

            # 상태 출력
            printall()
            if (now.hour % 3) == 0 and time_save:
                time_save = False
                msg = f"지금 {now.hour}시입니다. 코드가 잘 실행되고 있습니다."
                bot.sendMessage(mc,msg)
        except Exception as e:
            print(e)
            msg = e
            bot.sendMessage(mc,msg)
