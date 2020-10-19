# CovidUSUpdate
A python script that uses BeautifulSoup to get COVID-19 new cases in the US from Worldometer.info and uses Twilio to send SMS notification

# Installation
## Pre-requisites
You must have a Twilio account. You can use the free trial if you like.

You will need to install ConfigParser, Requests, BeautifulSoup4, and Twilio as Python modules. I use pip.

    pip install configparser requests beautifulsoup4 twilio

I've included a sample_config.ini file with the correct config identifiers and some dummy values. Replace them with your own and rename the file to config.ini