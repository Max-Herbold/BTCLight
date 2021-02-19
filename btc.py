import requests
import time
import json

class btc:
    def __init__(self):
        self.symbol = "BTCUSDC"
        self.url = "https://api.binance.com/api/v3/ticker/price?symbol="+self.symbol
        self.last = 0
    def getNextPrice(self):
        while 1:
            r = requests.get(self.url)
            if r.status_code != 200: return -1
            t = r.text
            j = json.loads(t)
            v = float(j['price'])
            if v != self.last:
                c = int(round(v-self.last,0))
                print(f'BTC PRICE: {v}USD - Change: {c}')
                self.last = v
                return c
            time.sleep(0.5)
