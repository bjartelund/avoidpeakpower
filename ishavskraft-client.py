from atd import atd
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from datetime import timedelta
from datetime import date
import json
with open("secret") as secret, open("user") as user:
    params={"password": secret.read().strip(),"username":user.read().strip()}
    r= requests.post("https://utvikler.ishavskraft.no//api/v1/token",json=params)
    token=r.json()["token"]
today=date.today()
tomorrow=date.today() + timedelta(days=1)
tomorrowplusone=date.today() + timedelta(days=2)
headers = CaseInsensitiveDict()

headers["Authorization"] = "Bearer %s" % token

request= requests.get("https://utvikler.ishavskraft.no/api/v1/spotpriser/%s/%s/NO4" % (today.isoformat(),tomorrow.isoformat()),headers=headers)
timedict=dict()
print(request.text)
for klokkeslett in request.json()["spotprisDagList"][0]["spotprisList"]:
    timedict[klokkeslett["time"]]=klokkeslett["pris"]

sortedtimedict={k: v for k, v in sorted(timedict.items(), key=lambda item: item[1])}
print(sortedtimedict)
highestprices=list(sortedtimedict)[-3:]
highestprices.sort()
print(highestprices)
prev=None
for hour in highestprices:
    hourobject=datetime.fromisoformat(hour)
    future=hourobject+timedelta(hours=1)
    if prev:
        difference=hourobject-prev
        if difference == timedelta(hours=1):
            print("continious")
        else:
            print("turn on again at %s" % (hourobject+timedelta(hours=1)))
    prev=hourobject
    print("Turning off at %s" % hour)
    atd.at("cd /home/bjarte/python/avoidpeakpower/ && ./heaters_off.py",hourobject.astimezone().replace(tzinfo=None))
            
print("turn on again at %s" % (hourobject+timedelta(hours=1)))
atd.at("cd /home/bjarte/python/avoidpeakpower/ && ./heaters_on.py",future.astimezone().replace(tzinfo=None))
