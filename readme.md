##Shows the change in BTC via WS2812 LED strip lights.

###Follow the tutorial to setup prerequisites.

```sudo apt-get update;sudo apt-get install gcc make build-essential python-dev git scons swig
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/python

sudo python3 setup.py build 
sudo python3 setup.py install 
sudo pip3 install adafruit-circuitpython-neopixel```
