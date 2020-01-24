from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib, json, requests
from requests import Request, Session
import time, datetime

coinID = None

# define a Coin class
class Coin(object):
    """a coin class"""
    def __init__(self):
        self.id = ""
        self.name = ""
        self.symbol = ""

# fetch all active cryptocurrencies by market cap and return market values in USD
def getListings():
    coinList = []

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'5000',
        'convert':'USD'
    }
    headers = {
        'Accepts':'application/json',
        'X-CMC_PRO_API_KEY':'2c16679d-c0a5-40fd-84c1-e06ca84b0b88'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        listing = json.loads(response.text)
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    for item in listing['data']:
        # print(item)
        listedCoin = Coin()
        listedCoin.name = str(item['name'])
        listedCoin.id = str(item['id'])
        listedCoin.symbol = str(item['symbol'])

        coinList.append(listedCoin)

    return coinList
        
# Create your views here.
def coins(request):
    getListings()

    if request.method == 'GET':
        template = loader.get_template('coinapp/coins.html')
        context = {
            'getListings' : getListings(),
        }
        return HttpResponse(template.render(context, request))

    elif request.method == 'POST':
        for item in request.body:
            print(item)
        return HttpResponse(request.POST['coinselected'])