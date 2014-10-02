#!/usr/bin/python
import paho.mqtt.client as mqtt
import os
import time
import re
import sys
import signal
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

broker = "192.168.1.3"
tcpport = 1883
topic = "house/temp/outside"
url = "http://jonarcher.info/weather-data"

mqttc = mqtt.Client()
mqttc.connect (broker, tcpport, 60)
mqttc.loop_start()
while True:

	response = urllib.urlopen(url);
	data = json.loads(response.read())
	temp = data["temperature"]
	mqttc.publish(topic,temp, retain=True)
	time.sleep(30)

mqttc.loop_forever()

if __name__ == "__main__":
    set_exit_handler(on_exit)
~

