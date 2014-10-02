#!/usr/bin/python

import sys,time,signal
import redis
import datetime
from time import sleep
import urllib
import json

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)

broker = "192.168.1.181"
tcpport = 6379
topic = "house/temp/outside"
url = "http://jonarcher.info/weather-data"

redthis = redis.StrictRedis(host='433board',port=6379, db=0)
def queue_weather(file):
    outside_temp=0
    redthis.set(topic,0) 
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    temp = data["temperature"]
    redthis.set(topic,temp) 
     
while True:
	queue_weather(url)
	time.sleep(50)

if __name__ == "__main__":
    set_exit_handler(on_exit)
