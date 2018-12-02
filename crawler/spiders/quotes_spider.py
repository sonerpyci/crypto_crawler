import scrapy
import time
#import datetime
#import urllib.parse as urlparse
import requests
#import geocoder
#from selenium import webdriver
#from selenium.webdriver.support.select import Select
#from selenium.webdriver.firefox.options import Options
#from selenium.common.exceptions import StaleElementReferenceException
#from selenium.common.exceptions import NoSuchElementException        
#from fake_useragent import UserAgent
#import random
#import traceback
import json
import sys

class Binance:
    base_url = "https://api.binance.com/api/v1/ticker/price?symbol="
    param = "BTC"
    def get_last_price(self, coin_ticker):
        req_url = self.base_url + coin_ticker + self.param
        response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
        data = response.json() # Check the JSON Response Content documentation below
        if 'price' in data:
            #print(data['price'])
            return data['price']
        else:
            return -1


class Bittrex:
    base_url = "https://bittrex.com/api/v1.1/public/getticker?market=BTC-"

    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url + coin_ticker
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if 'success' in data:
                if data['success'] == True:
                    #print(data['result']['Last'])
                    return(data['result']['Last'])
                else:
                    return -1
        except:
            print("No Currency Found Error")
            return -1

class BtcAlpha:
    base_url = "https://btc-alpha.com/api/v1/orderbook/"
    param = "_USD/?format=json"
    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url + coin_ticker + self.param
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if 'sell' in data:
                if len(data['sell']) > 0:
                    #print(data['sell'][-1]['price'])
                    return data['sell'][-1]['price']
                else:
                    return -1
            else:
                return -1
        except:
            print("No Currency Found Error")
            return -1

class CoinExchange:
    market_url = "https://www.coinexchange.io/api/v1/getmarkets"
    base_url = "https://www.coinexchange.io/api/v1/getmarketsummary?market_id="
    def get_market_list(self, coin_ticker):
        try:
            req_url = self.market_url
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            coin_list = data['result']
            for coin in coin_list:
                if coin['MarketAssetCode'] == coin_ticker:
                    return coin['MarketID']
        except:
            #print('"No currency Found" Error')
            return -1

    def get_last_price(self, coin_ticker):
        try:
            market_id = self.get_market_list(coin_ticker)
            req_url = self.base_url + str(market_id)
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if data['success'] == "1":
                #print(data['result']['LastPrice'])
                return data['result']['LastPrice']
            else:
                return -1
        except:
            print('"No currency Found" Error')
            return -1


class CryptoBridge:
    base_url = "https://api.crypto-bridge.org/api/v1/ticker/"
    param = "_BTC"   #request url should be like "...api/GetMarket/[coin_ticker]_BTC"
    def get_last_price(self, coin_ticker):
        req_url = self.base_url + coin_ticker + self.param
        response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
        data = response.json() # Check the JSON Response Content documentation below
        if "last" in data:
            #print(data["last"])
            return data["last"]
        else:
            return -1


class Cryptopia:
    base_url = "https://www.cryptopia.co.nz/api/GetMarket/"
    param = "_BTC"   #request url should be like "...api/GetMarket/[coin_ticker]_BTC"
    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url + coin_ticker + self.param
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if "Success" in data:
                if data['Success'] == True:
                    if data["Data"] != None:
                        #print(data["Data"]["LastPrice"])
                        return data["Data"]["LastPrice"]
                    else:
                        return -1
                else:
                    return -1
            else:
                return -1
        except:
            print("No Currency Found Error")
            return -1


class Graviex:
    base_url = "https://graviex.net//api/v2/tickers/"
    param = "btc.json"
    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url + coin_ticker.lower() + self.param
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if "error" not in data:
                if 'ticker' in data:
                    if 'last' in (data['ticker']):
                        #print(data['ticker']['last'])
                        return data['ticker']['last']
                    else:
                        return -1
                else:
                    return -1
            else:
                return -1
        except:
            print("No Currency Found Error")
            return -1
        


class Mercatox:
    base_url = "https://mercatox.com/public/json24"
    param = "_BTC"
    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            key = coin_ticker + self.param
            if key in data['pairs']:
                #print(data['pairs'][key]['last'])
                return data['pairs'][key]['last']
            else:
                return -1
        except:
            print("No Currency Found Error")
            return -1


class SouthExchange:
    base_url = "https://www.southxchange.com/api/price/"
    param = "/btc"   #request url should be like "...api/GetMarket/[coin_ticker]_BTC"
    def get_last_price(self,coin_ticker):
        try:
            req_url = self.base_url + coin_ticker + self.param
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            if "Last" in data:
                #print(data["Last"])
                return data["Last"]
            else:
                return -1
        except:
            print("No Currency Found Error")
            return -1

class Stex:
    base_url = "https://app.stex.com/api2/ticker"
    param = "_BTC"
    def get_last_price(self, coin_ticker):
        try:
            req_url = self.base_url
            coin_key = coin_ticker + self.param
            response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
            data = response.json() # Check the JSON Response Content documentation below
            for coin in data:
                if coin['market_name'] == coin_key:
                    #print(coin['last'])
                    return coin['last']
            return -1
        except:
            return -1

#from lxml.html.clean import Cleaner
class Coin_Crawler(scrapy.Spider):           
    name = "coin_crawler"
    cryptoCompareUrl = "https://masternodes.pro/apiv2/coin/stats/"
    #def __init__(self):
        #self.options = Options()
        #self.options.log.level = 'fatal'
        #self.driver = webdriver.Firefox()

    def get_crypto_compare_coin_stats(self, coinTicker):
        req_url = self.cryptoCompareUrl + coinTicker
        response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
        data = response.json() # Check the JSON Response Content documentation below
        print(data['stats']['cmc']['price_btc'])
        return data

    #def stale_aware_for_action(self, action):
    #    while(True):
    #        try:
    #            action()
    #            break
    #        except StaleElementReferenceException:
    #            continue
            
    def start_requests(self):
        urls = [
            'http://localhost:3000/registration'
        ]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, priority = 10)
    
    def switcher(self, argument):
        switcher = {
            "southxchange": SouthExchange,
            "cryptobridge": CryptoBridge,
            "cryptopia": Cryptopia,
            "btcalpha": BtcAlpha,
            "coinexchange": CoinExchange,
            "graviex": Graviex,
            "mercatox": Mercatox,
            "bittrex": Bittrex,
            "binance": Binance,
            "stocksexchange": Stex
        }
        return switcher[argument]
    def parse(self, response):
        registrations = json.loads(response.text)
        for registration in registrations:
            try:
                total_price = 0
                average_price = 0
                counter = 0
                xchg_list = registration['selectxchange'].split(',')
                for xchg in xchg_list:
                    #print('\t'* 2 + registration['coinName'].upper() + '\t'* 3 + xchg + '\n')
                    exchange_class = self.switcher(xchg)()
                    price = exchange_class.get_last_price(registration['coinTicker'])
                    print('\n')
                    if price != -1:
                        print('=================================================')
                        print(registration['coinName'].upper() + ' ' + xchg.upper() + " Price:" + str(price))
                        total_price += float(price)
                        counter += 1
                        print('=================================================')
                    else:
                        print('=================================================')
                        print("There is not any price info about {} in {}".format(registration['coinName'].upper(), xchg.upper()))
                        print('=================================================')
                    print('\n' * 2)
                coin_details = self.get_crypto_compare_coin_stats(registration['coinTicker'])
                
                average_price = total_price / counter
                print("**** {} Average Price: {} ****".format(registration['coinName'].upper(), average_price))
                data = {
                            "registration_id": registration["id"],
                            "coinTicker": registration["coinTicker"],
                            "coinName": registration["coinName"],
                            "coinLogo": registration["coinLogo"],
                            "currentPrice": average_price,
                            "collateralAmount": registration["collateralAmount"],
                            "isCrawled": True,
                            "worth": coin_details['stats']['masterNodeWorth'],
                            "dailyIncome": coin_details['stats']['income']['daily'],
                            "monthlyIncome": coin_details['stats']['income']['monthly'],
                            "yearlyIncome": coin_details['stats']['income']['yearly'],
                            "roi": coin_details['stats']['roi'],
                            "masternode_count": coin_details['advStats']['masterNodeCount'],
                            "percentChange24h": coin_details['stats']['cmc']['percent_change_24h'],
                            "rank": coin_details['stats']['cmc']['rank'],
                            "status": None,
                            "lastCheckTime": str(int(time.time()))
                        }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                req_to_insert = requests.post('http://localhost:3000/registered_coin', data=json.dumps(data), headers=headers)
                print(req_to_insert)
            except:
                print(sys.exc_info()[0])
                print(registration['coinTicker'])
                continue
        print("@@@@@@@@    sleeping 20 secs    @@@@@@@@")
                
            