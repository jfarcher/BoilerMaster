#!/usr/bin/python
import redis
import os
import time
import serial
import datetime
import re
import sys
import signal
from ConfigParser import SafeConfigParser
import paho.mqtt.client as mqtt

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

parser = SafeConfigParser()
parser.read('/etc/boilermaster/boilermaster.conf')  

rbroker = parser.get('redis', 'broker')
mbroker = parser.get('mqtt', 'broker')
rtcpport = parser.get('redis', 'port')
mtcpport = parser.get('mqtt', 'port')
baud = 115200
port = '/dev/ttyAMA0'
ser = serial.Serial(port, baud)
topic = parser.get('temps', 'topic')
mqttc = mqtt.Client()

mypid = os.getpid()

#Connect to broker
redthis = redis.StrictRedis(host=rbroker,port=rtcpport, db=0)
mqttc.connect (mbroker, mtcpport, 60)
                                                                                                                   

while True:
	llapMsg = ser.read(12)
        devID = llapMsg[1:3]
	sensor = llapMsg[3:7]
        temp = llapMsg[7:12]
	while temp.endswith("-"):
			temp = temp[:-1]
	if sensor == "TEMP":
		redthis.set(topic + devID + "/sensor",temp) 
		mqttc.publish(topic + devID + "/sensor",temp, retain=True)
