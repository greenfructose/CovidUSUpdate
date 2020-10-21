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
    # Get all table rows on page
    rows = soup.find_all('tr')
    # Create list to add numbers of cases to
    caseList = []
    deathList = []
    newResults = []
    # Iterate over rows, get table data for each row
    for row in rows:
        data = row.find_all('td')
        # Some rows have no table data, so we must check for it
        if data:
            # Check if this row is the row for USA
            if data[1].get_text() == "USA":
                # Format the number by removing the +sign and all commas
                newCaseStr = data[3].get_text()[1:].replace(",", "")
                deathStr = data[5].get_text()[1:].replace(",", "")
                # Check if numberStr is empty, Cast number string as int
                if newCaseStr == "":
                    caseNumber = 0
                else:
                    caseNumber = int(newCaseStr)
                if deathStr == "":
                    deathNumber = 0
                else:
                    deathNumber = int(deathStr)
                # Was getting multiple rows for this but should only be one, created these lists to add all values
                caseList.append(caseNumber)
                deathList.append(deathNumber)
    # Returns the new cases and new deaths as a list, first item in each list is correct data
    newResults.append(caseList[0])
    newResults.append(deathList[0])
    return newResults


if __name__ == '__main__':
    # Get config info from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    account_sid = config['API']['account_sid']
    auth_token = config['API']['auth_token']
    receiver = config['sms']['receiver']
    sender = config['sms']['sender']
    # Initialize Twilio client
    client = Client(account_sid, auth_token)
    # Variables to compare whether or not new cases have been added since last check
    results = []
    startCases = 0
    newCases = 0
    while True:
        results = getUpdate()
        newCases = results[0]
        newDeaths = results[1]
        if newCases != startCases:
            now = datetime.now()
            date_time = now.strftime("%H:%M:%S")
            print("The US has {} new cases and {} new deaths as of {}".format(newCases, newDeaths, date_time))
            # Create the SMS message to be sent
            message = client.messages.create(
                to=receiver,
                from_=sender,
                body="As of {}, there are {} new Covid-19 cases in the US today and {} new Covid-19 deaths.".format(date_time, newCases, newDeaths)
            )
            # Send message and reset case counts
            print(message.sid)
            startCases = newCases
        # Wait 10 minutes before checking if new cases have been added
        time.sleep(1800.0)

