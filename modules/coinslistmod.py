import requests
import json
import pandas as pd

url = "https://api.upbit.com/v1/market/all"
querystring = {"isDetails":"true"}
headers = {"Accept": "application/json"}
res = requests.request("GET", url, headers=headers, params=querystring)
jt = json.loads(res.text)
df = pd.DataFrame.from_dict(jt)
print(df)
