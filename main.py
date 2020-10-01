from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import urllib.request
import config
from tkinter import *


chatBotApiKey=config.chatBotApiKey


def receivedErrorWeather():
    return "Couldn'tGetWeatherInformation."

def convertWeatherInfo(data):
    theJSON = json.loads(data)
    weatherString=str(round(theJSON["main"]["temp_min"]-273.15,1))+"-"+str(round(theJSON["main"]["temp_max"]-273.15,1))
    return weatherString

def getWeatherString():
    myapikey = config.myapikey
    city='Bucharest'
    weatherString=''

    try:
        urlData = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + myapikey
        print(urlData)
        webUrl = urllib.request.urlopen(urlData)
        if (webUrl.getcode() == 200):
            data = webUrl.read()
            weatherString=convertWeatherInfo(data)
        else:
            weatherString=receivedErrorWeather()
    except:
        weatherString=receivedErrorWeather()
    finally:
        return weatherString


def emailInfo():
    global msg
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    #Here you should start configuring the code

    # Call the Gmail API
    results= service.users().messages().list(userId='me',labelIds=['INBOX'],q="is:unread").execute()
    messages = results.get('messages',[])

    if not messages:
        return "NoNewEmails"
    else:
        message_count= 0
        for message in messages:
            msg = service.users().messages().get(userId='me',id=message["id"]).execute()
            message_count+=1
        messageString=str(message_count)+"UnreadEmails"
        #Display number of emails
        urllib.request.urlopen(
            'https://api.callmebot.com/whatsapp.php?phone=+40727587574&text='+messageString+'&apikey='+chatBotApiKey)


def convertExchangeInfo(data):
    theJSON = json.loads(data)
    exchangeString = "EUR:1->RON:" +str(round(theJSON["rates"]["RON"],2))
    return exchangeString

def receivedErrorExchange():
    return "Couldn'tGetExchangeRateInformation"

def exchangeRateInfo():
    exchangeApiKey=config.exchangeApiKey
    exchangeString=''
    try:
        urlData = "http://data.fixer.io/api/latest?access_key=" + exchangeApiKey
        webUrl = urllib.request.urlopen(urlData)
        if (webUrl.getcode() == 200):
            data = webUrl.read()
            exchangeString=convertExchangeInfo(data)
        else:
            exchangeString=receivedErrorExchange()
    except:
        exchangeString=receivedErrorExchange()
    finally:
        return exchangeString

def sendWeatherInfo():
    weatherBody=''
    #Weather
    weatherBody+=getWeatherString()
    #Display weather
    urllib.request.urlopen('https://api.callmebot.com/whatsapp.php?phone=+40727587574&text='+weatherBody+'&apikey='+chatBotApiKey)

def sendGmailInfo():
    emailInfo()

def sendExchangeInfo():
    exchangeBody=exchangeRateInfo()
    urllib.request.urlopen(
        'https://api.callmebot.com/whatsapp.php?phone=+40727587574&text=' +exchangeBody+ '&apikey='+chatBotApiKey)

def main():
    root = Tk()
    root.title("Phone Connector")
    root.geometry('400x350')
    root.configure(background='white')
    #3 buttons
    #weather
    sendWeatherButton = Button(root, text="Send Weather", font=('Arial', 13, 'bold'), padx=100, pady=20,
                              command=sendWeatherInfo, background='lightblue')
    sendWeatherButton.pack(pady=20)
    #emails
    sendEmailInfoButton=  Button(root,text="Send Email Info",font=('Arial', 13, 'bold'), padx=100, pady=20,
                              command=emailInfo, background='lightblue')
    sendEmailInfoButton.pack(pady=20)
    #EUR - RON
    sendExchangeRateButton = Button(root,text="Send Email Info",font=('Arial', 13, 'bold'), padx=100, pady=20,
                              command=sendExchangeInfo, background='lightblue')
    sendExchangeRateButton.pack(pady=20)

    root.mainloop()


if __name__=='__main__':
    main()
