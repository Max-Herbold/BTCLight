import requests
import time
import json

class btc:
    def __init__(self):
        self.currency = "AUD" # USDC for usd price
        self.symbol = "BTC" + self.currency
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol="+self.symbol
        self.last = 0
        self.s = 200

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
                print(f'BTC PRICE: {v}{self.currency} - Change: {c}')
                self.last = v
                return c
#            else:
#                print(f"same: {v}")
            time.sleep(0.1)

class failedGet(Exception):
    def __init__(self, status):

        self.message = f"Failed to get value from API endpoint. (Status code: {status})"
        print(self.message)
