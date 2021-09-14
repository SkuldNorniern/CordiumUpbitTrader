import csv
from modules import configmod as cfm
from modules import loggermod as lgm

def init():
    whl = cfm.whitelist_read()
    coin_list = whl.split(',')
    n=len(coin_list)
    lgm.logmsg('Coinlist is updated writing changes.','info')
    with open('dataset.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['coin', 'target', 'money_list', 'hold', 'op_mode', 'yesterday_ma15', 'open_price'])
        for i in range(n):
            msg='Writing '+coin_list[i]+' on the list.'
            lgm.logmsg(msg,'debug')
            spamwriter.writerow([coin_list[i], '1E+15', '-1', 'FALSE', 'FALSE', '0', '0'])
    cfm.isupdated_write()

def init_savedata():
    lgm.logmsg('Generating Saved_data file.','info')
    with open('saved_data.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['', 'date', 'jonbeo', 'auto_upbit', 'difference_jonbeo_autoupbit' ,'difference_yesterday'])
