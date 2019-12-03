# [raspberry-pi-glowing-weather](https://github.com/rickhewes/raspberry-pi-glowing-weather/)

[Raspberry pi](https://www.raspberrypi.org) and [unicorn pHAT](https://github.com/pimoroni/unicorn-hat) glowing weather indicator. Downloads observational and 3 day forecast weather feed from the [BBC Weather](http://www.bbc.co.uk/weather/about/17543675) and displays the data as a temperature map.

Here is the display in action:

![alt text](https://github.com/rickhewes/raspberry-pi-glowing-weather/blob/master/assets/glowing-weather.jpg "zero pi glow weather")

Here is the temperature map that is used for the observational and 3 day forecast data:

![alt text](https://github.com/rickhewes/raspberry-pi-glowing-weather/blob/master/assets/temperature-map.png "temperature map")

## Installation

Install the support library for the unicorn-hat if you haven't already:
```bash
curl -sS https://get.pimoroni.com/unicornhat | bash
```

Optional, install the unicorn hat [simulator](https://github.com/jayniz/unicorn-hat-sim) (for running without the unicorn-hat on a desktop):
```
sudo pip3 install git+git://github.com/adamkaplan/unicorn-hat-sim@patch-1#egg=unicorn-hat-sim
```

Clone and run the python script;
```bash
git clone https://github.com/rickhewes/raspberry-pi-glowing-weather/
cd raspberry-pi-glowing-weather
sudo ./glowing-weather.py
```

## Change the location id

Set your own location id by finding your town on the [BBC Weather](https://www.bbc.co.uk/weather) page and copying the code found at the end of the url into the file. e.g. https://www.bbc.co.uk/weather/0/2656171

```python
locationId = "2656171"
```
