import requests
import time
import json
import datetime

class btc:
    def __init__(self):
        self.currency = "AUD" # USDC for usd price
        self.symbol = "BTC" + self.currency
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol="+self.symbol
        self.last = 0
        self.s = 200
        self.log_file = "/home/pi/BTCLight/log.txt"

    def log(self,string):
        f = open(self.log_file, 'a')
        f.write(str(string) + "\n")
        f.close()

    def getNextPrice(self):
        while 1:
            r = requests.get(self.url)
            self.s = r.status_code
            if r.status_code != 200: raise failedGet(r.status_code)
            t = r.text
            j = json.loads(t)
            v = float(j['price'])
            if v != self.last:
                c = int(round(v-self.last,0))
                self.log(f'{datetime.datetime.now()} - ${v}{self.currency} - c: {c}')
                self.last = v
                return c
            time.sleep(0.1)

class failedGet(Exception):
    def __init__(self, status):
        self.message = f"{datetime.datetime.now()} - Failed to get value from API endpoint. (Status code: {status})"
        btc().log(self.message) # create new object to log to same location... kinda iffy