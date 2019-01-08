#!/usr/bin/env python

import pandas as pd
from datetime import datetime, timedelta
import time
import requests
import json
import logging

logging.basicConfig(filename='markethistory3.log',level=logging.DEBUG)

shouldRun = True
if datetime.now().minute not in {0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}:
 shouldRun = False

while True:
    if shouldRun == False:
        current_time = datetime.now()
        seconds = 60 - current_time.second
        minutes = current_time.minute + 1
        snooze = ((5 - minutes%5) * 60) + seconds
        logging.info('minutes:%s seconds:%s sleep:%s', minutes, seconds, snooze)
	localtime = time.asctime( time.localtime(time.time()))
        logging.info('sleeping at %s', localtime)
        time.sleep(snooze)  # Sleep until next quarter hour.
        shouldRun = True
    else:
        localtime = time.asctime( time.localtime(time.time()))
        logging.info("time to check data... wait for 1 minute before begin...")
	time.sleep(60) #check at 5 & 35 minutes of an hour
        
	#get historical market data
	URL = "https://bittrex.com/Api/v2.0/pub/market/GetTicks"
	market = "BTC-ETH"
	interval = "fiveMin"
	timestamp = "1500915289433"
	PARAMS = {'marketName':market, 'tickInterval':interval, '_':timestamp}
	r = requests.get(url = URL, params = PARAMS)
	data = r.json()
	df_NewData = pd.DataFrame(data['result'])
	
	#check if theres new data
	df_OldData = pd.read_csv('data_pandas.csv')
	LastRecTime =  df_OldData.loc[df_OldData.index[-1], "T"]
	t_LastRecTime = datetime.strptime(LastRecTime, "%Y-%m-%dT%H:%M:%S")
	LatestTime =  df_NewData.loc[df_NewData.index[-1], "T"]
	t_LatestTime = datetime.strptime(LatestTime, "%Y-%m-%dT%H:%M:%S")
	logging.info('LastRecTime:%s',LastRecTime)
	logging.info('LatestTime:%s',LatestTime)
	if t_LatestTime > t_LastRecTime :
 	 logging.info('time to update market')
	 df_NewData.tail(1).to_csv('data_pandas.csv', mode='a', header=False)
	 LastRecTime = df_NewData.loc[df_NewData.index[-1], "T"]
	 t_LastRecTime = datetime.strptime(LastRecTime, "%Y-%m-%dT%H:%M:%S")

        shouldRun = False

