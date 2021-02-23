## Shows the change in BTC via WS2812 LED strip lights.

### Follow the tutorial to setup prerequisites.

```
sudo apt-get update;sudo apt-get apt-listchanges install python3-pip python3-distutils gcc make build-essential python-dev git scons swig

git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x
sudo scons
cd python
sudo python3 setup.py build 
sudo python3 setup.py install

sudo python3 -m pip install adafruit-circuitpython-neopixel
```
