import requests
import json
import pandas as pd

df = pd.DataFrame(columns=["name","craft"])

url = "http://api.open-notify.org/astros.json"

headers = {}
payload = {}

resp = requests.get(url=url,headers=headers,data=payload)
print (resp.status_code)
space_folks = json.loads(resp.text)
print (space_folks)

for item in space_folks["people"]:
    df.loc[len(df.index)] = item

print (df)
