#!/usr/bin/python
import paho.mqtt.client as mqtt
import os, sys, time, signal
import re
import urllib, json
from ConfigParser import SafeConfigParser

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
broker = parser.get('mqtt', 'broker')
tcpport = parser.get('mqtt', 'port')
url = parser.get('weather', 'url')
topic = parser.get('weather', 'topic')

mqttc = mqtt.Client()
mqttc.connect (broker, tcpport, 60)
mqttc.loop_start()
while True:
	try:
		response = urllib.urlopen(url);
		data = json.loads(response.read())
		temp = data["temperature"]
	except:
		temp = "100"
	mqttc.publish(topic,temp, retain=True)
	time.sleep(30)

mqttc.loop_forever()

if __name__ == "__main__":
    set_exit_handler(on_exit)

