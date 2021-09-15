import csv
import os.path
from modules import configmod as cfm
from modules import loggermod as lgm
file_dts = 'dataset.csv'
file_svr = 'saved_report.csv'

def init():
    lgm.logmsg('Start Initialing data module','debug')
    if os.path.exists(file_dts):
        lgm.logmsg('Dataset Detected Continue to boot.','info')
    else:
        init_dataset()

    if os.path.exists(file_svr):
        lgm.logmsg('Report file Detected Continue to boot.','info')
    else:
        init_savereport()

def init_dataset():
    lgm.logmsg('Generating dataset.','warn')
    with open('dataset.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['coin', 'average', 'hold'])

def init_savereport():
    lgm.logmsg('Generating saved_report file.','warn')
    with open('saved_report.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['date','coin', 'action', 'amount','average','balance'])

def data_update(coin_name,avg,hold):
    lgm.logmsg('Updating dataset.','info')
    f = open('dataset.csv', 'r', newline='')
    rd=csv.reader(f)
    is_here=False
    lines=[]
    for i in rd:
        if i[0] ==coin_name:
            is_here=True
            i[1]=avg
            i[2]=hold
        lines.append(i)
    if is_here==True:
        f = open('dataset.csv', 'w', newline='')
        wr=csv.writer(f)
        wr.writerows(lines)
        f.close()
    else :
        f = open('dataset.csv', 'a', newline='')
        wr=csv.writer(f)
        wr.writerow([coin_name,avg,hold])
        f.close()

def data_remove(coin_name):
    lgm.logmsg('Checking data for removal from dataset.','info')
    f = open('dataset.csv', 'r', newline='')
    rd=csv.reader(f)
    lines=[]
    for i in rd:
        if i[0] !=coin_name:
            lines.append(i)
            msg = "chk %s to %s"%(coin_name,i[0])
            lgm.logmsg(msg,"debug")
        else:
            lgm.logmsg(coin_name,"debug")
    f = open('dataset.csv', 'w', newline='')
    wr=csv.writer(f)
    wr.writerows(lines)
    f.close()


def report_update(date,coin_name,action,amount,avg,balance):
    lgm.logmsg('Updating report.','info')
    f = open('saved_report.csv', 'a', newline='')
    wr=csv.writer(f)
    wr.writerow([date,coin_name,action,amount,avg,balance])
    f.close()

def watching_list():
    lgm.logmsg('Reading dataset.','info')
    f = open('dataset.csv', 'r', newline='')
    rd=csv.reader(f)
    lines=[]
    for i in rd:
        lines.append(i)
    msg='Count of Watchlist is %d.'%(len(lines))
    lgm.logmsg(msg,'debug')
    return len(lines)
