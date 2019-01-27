from os import system
import time
import sys
from threading import Thread

def run_crawler():

    system('pkill chromedriver')
    system('pkill chrome')
    system('pkill Xvfb')
	
    if "development" in sys.argv:
        system('scrapy crawl coin_crawler') # for easy debug
    else:
        system('scrapy crawl -s LOG_ENABLED=False coin_crawler')

if __name__ == '__main__':
    if "development" in sys.argv:
        print("Crawler Running Development Mode.\n==>\t You can see all Process details in Console\n")
    else:
        print("Crawler Running Normal Mode.\n==>\t You can add 'development' word to reach specific Process details\n")
    while True:
        Thread(target = run_crawler).start()
        time.sleep(1200) # 20 minutes
