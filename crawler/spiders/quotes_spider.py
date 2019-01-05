import scrapy
import time
#import datetime
#import urllib.parse as urlparse
import requests
#import geocoder
from selenium import webdriver
#from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException        
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display

#from fake_useragent import UserAgent
#import random
#import traceback
import json
import sys
import linecache

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
        if response.status_code != 200:
            return -1
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
            if len(response.text.replace('"','')) == 0:
                return -1
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
    cryptoCompareUrl = "https://masternodes.pro/apiv2/coins/stats?currency=null"
    masternodes_pro_base_url= "https://masternodes.pro/"
    masternodes_pro_base_url2= "https://masternodes.pro/statistics"
    masternodes_pro_coin_url = "https://masternodes.pro/stats/"
    param = "/statistics"
    data = {}

    def phantom_settings_function(self):
        # PhantomJS settings
        phantom_settings = dict(DesiredCapabilities.PHANTOMJS)
        phantom_settings['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')
        phantom_settings['userAgent'] = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')
        phantom_settings['User-Agent'] = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')
        phantom_settings['phantomjs.page.settings.javascriptEnabled'] = True,   
        phantom_settings['phantomjs.page.settings.loadImages'] = True,
        phantom_settings['browserName'] = 'Google Chrome'
        phantom_settings['platformName'] = 'Linux'
        return phantom_settings
        
    def init_phantomjs_driver(self, *args, **kwargs):
    
        headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Connection': 'keep-alive'
        }
    
        for key, value in enumerate(headers):
            webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    
        driver =  webdriver.PhantomJS(*args, **kwargs)
        driver.set_window_size(1400,1000)
        print(webdriver.DesiredCapabilities.PHANTOMJS)
        return driver
        
    def __init__(self):
        display = Display(visible=0, size=(1366, 768))
        display.start()
        self.options = Options()
        self.options.add_argument("headless")
        self.options.add_argument('--disable-gpu')
        self.options.headless = True
        self.options.set_headless(headless=True)
        self.options.add_argument("headless") # Runs Chrome in headless mode.
        self.options.add_argument('--no-sandbox') # Bypass OS security model
        self.options.add_argument('start-maximized') # 
        self.options.add_argument('disable-infobars')
        self.options.add_argument("--disable-extensions")
        self.headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'Cache-Control':'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
        }
        for key, value in enumerate(self.headers):
            capability_key = 'phantomjs.page.customHeaders.{}'.format(key)
            webdriver.DesiredCapabilities.PHANTOMJS[capability_key] = value
        self.driver = webdriver.Chrome(chrome_options=self.options)#(desired_capabilities=self.phantom_settings_function(),service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])
        #self.driver = self.init_phantomjs_driver()
        #self.driver = webdriver.PhantomJS(desired_capabilities =self.phantom_settings_function(), service_args=['--ignore-ssl-errors=true', '--ssl-protocol=tlsv1'])

    def get_crypto_compare_coin_stats(self, coinTicker):
        req_url = self.cryptoCompareUrl
        response = requests.get(url=req_url) # özel durumlar için url yanına ,param=param parametresi de eklenebilir
        data = response.json() # Check the JSON Response Content documentation below
        for coin in response.data:
            if coin['coin'] == coinTicker:
                return data
        

    def stale_aware_for_action(self, action):
        while(True):
            try:
                action()
                break
            except StaleElementReferenceException:
                continue
            
    def start_requests(self):
        urls = [
            'http://localhost:3000/registration/IncludePassive'
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
    
    def PrintException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    
    
    
    def parse(self, response):
        registrations = json.loads(response.text)
        for registration in registrations:
            try:
                total_price = 0
                average_price = 0
                counter = 0
                xchg_list = registration['selectxchange'].split(',')
                for xchg in xchg_list:
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

                self.driver.get(self.masternodes_pro_base_url)
                self.driver.implicitly_wait(10)
                self.driver.get(self.masternodes_pro_base_url2)
                self.driver.set_window_size(1120, 550)
                time.sleep(5)
                print(self.driver.page_source)
                self.driver.set_window_size(1400,1000)
                self.driver.maximize_window()
                time.sleep(5)
                self.driver.save_screenshot('out.png');
                coin_link = self.driver.find_element_by_xpath('//*[@id="stats"]/tbody/tr/td/a[contains(text(), "{}")]'.format(registration['coinTicker']))
                coin_row = coin_link.find_element_by_xpath('./../..')
                percentChange24h = coin_row.find_element_by_xpath('./td[5]/span').text.replace(' ','').replace('%', '')
                self.driver.get(self.masternodes_pro_coin_url + registration['coinTicker'] + self.param)
                time.sleep(5)
                worth = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[1]/div[4]/mnp-data-box/div/div/div/div[1]/h3').text.replace(' ', '')
                dailyIncome = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[4]/div[1]/mnp-data-box/div/div/div/div[1]/h3/small').text.replace(' ', '')
                monthlyIncome = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[4]/div[3]/mnp-data-box/div/div/div/div[1]/h3/small').text.replace(' ', '')
                yearlyIncome = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[4]/div[4]/mnp-data-box/div/div/div/div[1]/h3/small').text.replace(' ', '')
                roi = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[1]/div[1]/mnp-data-box/div/div/div/div[1]/h3').text.replace(' ', '').replace('%', '')
                masternode_count = self.driver.find_element_by_xpath('//*[@id="mainbody"]/app-root/mnp-stats-base/div/div/mnp-advanced-stats/div/div[1]/div[1]/div[4]/mnp-data-box/div/div/div/div[1]').text.replace(' ', '')

                average_price = total_price / counter
                print("**** {} Average Price: {} ****".format(registration['coinName'].upper(), average_price))
                self.data = {
                            "registration_id": registration["id"],
                            "coinTicker": registration["coinTicker"],
                            "coinName": registration["coinName"],
                            "coinLogo": registration["coinLogo"],
                            "currentPrice": average_price,
                            "collateralAmount": registration["collateralAmount"],
                            "isCrawled": True,
                            "worth": worth,
                            "dailyIncome": dailyIncome.replace(registration['coinTicker'].lower(), '').replace(registration['coinTicker'].upper(), '').replace(',','.'),
                            "monthlyIncome": monthlyIncome.replace(registration['coinTicker'].lower(), '').replace(registration['coinTicker'].upper(), '').replace(',','.'),
                            "yearlyIncome": yearlyIncome.replace(registration['coinTicker'].lower(), '').replace(registration['coinTicker'].upper(), '').replace(',','.'),
                            "roi": roi,
                            "masternode_count": masternode_count,
                            "percentChange24h": percentChange24h,
                            # "rank": coin_details['stats']['cmc']['rank'],
                            "status": None,
                            "lastCheckTime": str(int(time.time()))
                        }
                print(self.data)
                
            except:
                self.PrintException()
                print(registration['coinTicker'])
                continue
            finally:
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                req_to_insert = requests.post('http://localhost:3000/registered_coin', data=json.dumps(self.data), headers=headers)
                print(req_to_insert.text)
        self.driver.close()
        display.stop()
        print("@@@@@@@@    sleeping 20 secs    @@@@@@@@")
            