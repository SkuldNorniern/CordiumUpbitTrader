import os
import jwt
import uuid
import hashlib
from modules import loggermod as lgm
from modules import configmod as cfm
from urllib.parse import urlencode

import requests

access_key = ''
secret_key = ''
server_url = ''

def init_account():
    lgm.logmsg('Loading upbit accounts data.','debug')
    access_key,secret_key,server_url = cfm.keys_read()
    msg='Access key '+access_key+ ' loaded.'
    lgm.logmsg(msg,'info')
    msg='Secret key '+secret_key+ ' loaded.'
    lgm.logmsg(msg,'info')
    msg='Server url '+server_url+ ' loaded.'
    lgm.logmsg(msg,'info')


def account_req():
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/accounts", headers=headers)
    print(res.json())
    return(res.json())


def init
