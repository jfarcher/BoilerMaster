#!/usr/bin/python
import paho.mqtt.client as mqtt
import redis
import datetime
import re
import sys, time, signal, os
from time import sleep
from ConfigParser import SafeConfigParser
import urllib, json


def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)
def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)

parser = SafeConfigParser()
parser.read('/etc/boilermaster/config.ini')
mbroker = parser.get('mqtt', 'broker')
mtcpport = parser.get('mqtt', 'port')
rbroker = parser.get('redis', 'broker')
rtcpport = parser.get('redis', 'port')

url = parser.get('weather', 'url')
topic = parser.get('weather', 'topic')  

redthis = redis.StrictRedis(host=rbroker,port=rtcpport, db=0)
mqttc = mqtt.Client()
mqttc.connect (mbroker, mtcpport, 60)
mqttc.loop_start()
while True:
	try:
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		temp = data["temperature"]
	exclude:
		temp = "100"
	mqttc.publish(topic,temp, retain=True)
    	redthis.set(topic,temp) 
	time.sleep(30)

mqttc.loop_forever()

if __name__ == "__main__":
    set_exit_handler(on_exit)
