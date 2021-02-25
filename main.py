#!/usr/bin/env python3

import btc
import time
from rpi_ws281x import *
import threading
import requests
import datetime
import math

# LED strip configuration:
LED_COUNT      = 109      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, change, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(change):
        strip.setPixelColor(i, color)
        if wait_ms != 0:
            strip.show()
            time.sleep(wait_ms/1000.0)
        if i > strip.numPixels():
            break
    strip.show()

def backwardsWipe(strip, clearTo, prev, wait_ms=50):
    opp = (clearTo < 0) ^ (prev < 0) # checks if the two are on opposite sides
    for i in range(strip.numPixels(), abs((not opp) * clearTo)-1, -1):
        strip.setPixelColor(i, Color(0,0,0))
        if wait_ms != 0:
            strip.show()
            time.sleep(wait_ms/1000.0)

def update(strip,c,prev,colors,delay):
    backwardsWipe(strip,c,prev,delay)
    colorWipe(strip,colors[int(c>0)],abs(c),delay)

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

b = 10 # brightness (0-255)
d = 0 # delay in ms

red = Color(b,0,0)
green = Color(0,b,0)
colors= [red,green]

prev = 0
coin = btc.btc()

first = True
change = 0

def quit():
    coin.log(f"Change during this run: {change}")
    backwardsWipe(strip,0,Color(0,0,0),d)
    strip.show()

def updateB():
    global b
    while 1:
        d = datetime.datetime.now()
        day = d.day+(d.month-1)*30                   # gets the day of the year aprox
        from_time = 2*math.cos(2*day*math.pi/365)+19 # will range from about 5 - 9pm
        to_time = 9                                  # not too fussed what the end time is.
        h = d.hour + d.minute / 60                   # gets the hour of day with decimal
        b = int(255 - 254 * from_time < h | h < to_time)
        time.sleep(60)

# TODO slot in updating b -- only need to do it once per minute buttt hmmmmm or even less.....
# that should be okay now...

brightness = threading.Thread(target=updateB)
brightness.start()

while 1:
    try:
        while 1:
            c = coin.getNextPrice()
            if not first:
                change += c
            else:
                first = False
            upd = threading.Thread(target=update, args=(strip,c,prev,colors,d))
            upd.start()
            prev = c

    except KeyboardInterrupt: # this handles process kill requests aswell.
        quit()
        break
    except requests.exceptions.ConnectionError:
        coin.log(f"Some error connecting occurred. http status: {coin.s}")
        time.sleep(1)
    except btc.failedGet:
        pass
