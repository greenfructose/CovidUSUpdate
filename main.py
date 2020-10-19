import configparser
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup
from twilio.rest import Client


def getUpdate():
    """Gets new daily Covid-19 cases for the US from https://www.worldometers.info/coronavirus/"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    url = "https://www.worldometers.info/coronavirus/"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    rows = soup.find_all('tr')
    rowList = []
    for row in rows:
        data = row.find_all('td')
        if data:
            if data[1].get_text() == "USA":
                numberStr = data[3].get_text()[1:].replace(",", "")
                number = int(numberStr)
                rowList.append(number)
    return rowList[0]


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    account_sid = str(config['API']['account_sid'])
    auth_token = str(config['API']['auth_token'])
    receiver = str(config['comms']['receiver'])
    sender = str(config['comms']['sender'])
    client = Client(account_sid, auth_token)
    startCases = 0
    newCases = 0
    while True:
        newCases = getUpdate()
        if newCases > startCases:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            print("The US has {} new cases as of {}".format(newCases, date_time))
            message = client.messages.create(
                to=receiver,
                from_=sender,
                body="As of {}, there are {} new Covid-19 cases in the US today.".format(date_time, newCases)
            )
            print(message.sid)
            startCases = newCases
        time.sleep(60.0)

