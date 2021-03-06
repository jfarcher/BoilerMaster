BoilerMaster
============

Set of scripts and applications to build a thermostat using a Raspberry Pi

Some of the contents of this application are derived from PiThermostat by TommyBobbins
https://github.com/tommybobbins/PiThermostat


Copy the config sample file to /etc/boilermaster/boilermaster.conf and edit

	sudo mkdir /etc/boilermaster

	sudo cp boilermaster.conf.sample /etc/boilermaster/boilermaster.conf

Weather
=======

These scripts allow the retrieval of weather data from external sources (currently only a json) and republish the temperature data retrieved to a redis or mqtt broker.

Installation: 
take the desired version mqtt or redis and copy the file to /usr/local/sbin/parse_weather_json.py

	cp utilities/weather/parse_weather_json_mqtt.py /usr/local/sbin/parse_weather_json.py
or

	cp utilities/weather/parse_weather_json_redis.py /usr/local/sbin/parse_weather_json.py

then copy the parse_weather file to /etc/init.d/

	cp utilities/weather/parse_weather.debian /etc/init.d/

or

	cp utilities/weather/parse_weather.rhel /etc/init.d/
	
Add the relevant details to the config file for the mqtt or redis servers on your network, and the topics you want to publish to

you can now start  the script with:

	service parse_weather start

and permanently enable it with:

	update-rc.d -f parse_weather defaults

or

	chkconfig parse_weather on
