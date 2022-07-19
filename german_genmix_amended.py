import pandas as pd
import json
import os
import requests
import time
import csv
from datetime import datetime, date, timedelta

begin_date = date.today() - timedelta(days = 180)
outputs = []

while begin_date < date.today():
    if begin_date < date.today() - timedelta(days = 7):
        begin_date = begin_date + timedelta(days = 7)
    else:
        begin_date = date.today()

    year = str(begin_date.year)
    weeknum = begin_date.strftime("%V")


#print(begin_date, weeknum, year)

    for item in weeknum:
        url = "https://energy-charts.info/charts/energy/data/de/day_week_" + year + "_" + weeknum + ".json"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
        r = requests.get(url, headers=headers)


        Date = [datetime.strptime(str(i), "%d.%m.%Y").strftime("%d/%m/%Y") for i in r.json()[0]["xAxisValues"]]
        blan = r.json()[1]["data"]
        hror = r.json()[3]["data"]
        biom = r.json()[4]["data"]
        nuke = r.json()[2]["data"]
        lign = r.json()[5]["data"]
        coal = r.json()[6]["data"]
        oil = r.json()[7]["data"]
        gas = r.json()[8]["data"]
        othr = r.json()[12]["data"]
        hwr = r.json()[10]["data"]
        winf = r.json()[16]["data"]
        wino = r.json()[17]["data"]
        sola = r.json()[18]["data"]
        load = r.json()[19]["data"]

        outputs.append(Date)

        print(Date, blan, nuke, biom, lign, coal, oil, gas, winf, wino, sola, load)

        df = pd.DataFrame(list(zip(Date, blan, hror, biom, nuke, lign, coal, oil, gas, othr, hwr, winf, wino, sola, load)), columns=['Date', 'Import (-), Export (+)', 'Hydro Run-of-River', 'Biomass', 'Nuclear', 'Fossil Brown Coal', 'Fossil Hard Coal', 'Fossil Oil', 'Fossil Gas', 'Others', 'Hydro Water Reservoir', 'Wind Offshore', 'Wind Onshore', 'Solar', 'Load'])
        df = df.set_index('Date')
        df.to_csv('german_genmix_' + year + '_' + weeknum + '.csv')

