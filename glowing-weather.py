#!/usr/bin/env python

import time
import requests
import unicornhat as unicorn
import re
import sys
import os

print("""Glowing Weather

Gets the current observational and 3 day forecast data from the BBC Weather and displays an appropriate colour

https://github.com/rickhewes/raspberry-pi-glowing-weather

If you're using a Unicorn HAT and only half the screen lights up,
edit this example and  change 'unicorn.AUTO' to 'unicorn.HAT' below.
""")

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(0.4)
width,height=unicorn.get_shape()

#South Wraxall
locationId = "2637274"

colourMapTemperatureBbc = ['3EC3FB','34C3FB','34C3FB','34C3FB','34C3FB','2DC5FB','97F6B0','97F7AE','9AF6AE','BAF373','BDF66F','BCF972','DDF969','D5F959','DDF968','FFF55E','FEF763','FFF65C','FFE45A','FFD955','FFD955','FFCA4F','FFCA4F','FFCA4F','FFAE49','FFAF4A','FFAF4A','FF983F','FF983F','FF983F','FF8639','FF893A','FF863B','FF8939','FF8637','FD823D','FF832F','FF8439','FF8A3A','FF862F','FF862F','FF862F','FF862F','FF862F','FF862F','FF862F']
colourMapTemperatureMetOffice = ['0000FF','007EFF','007EFF','00BEFF','00BEFF','00FFFF','00FFFF','00F7C6','00F7C6','18D78C','18D78C','00AA64','00AA64','2BAA2B','2BAA2B','2BC82B','2BC82B','00FF00','00FF00','CCFF00','CCFF00','FFFF00','FFFF00','EDED7E','EDED7E','E4CC66','E4CC66','DCAE49','DCAE49','FFAA00','FFAA00','FF5500','FF5500','FF0000','FF0000','C80000','C80000','AD0000','AD0000','930000','930000','780000','780000','780000','780000','780000']
colourMapWindSpeed = ['47B3E6','47B8D7','47B8D7','62BECA','81C4BC','81C4BC','99C7AE','99C7AE','99C7AE','AACFA0','AACFA0','AACFA0','BBD492','BBD492','BBD492','CBD889','CBD889','CBD889','DCDC85','DCDC85','DCDC85','E0C87F','E0C87F','E0C87F','E0A776','E0A776','E0A776','E0A776','E0A776','E0A776','E0866F','E0866F','E0866F','E0866F','E0866F','E0866F','E0686B','E0686B','E0686B','E0686B','E0686B','E0686B','DC5E85','DC5E85','DC5E85','DC5E85','DC5E85','DC5E85','DC5E85','DC5E85','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','C76AD1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1','AC68A1']

#Set our colour map
colourMapTemperature = colourMapTemperatureBbc #colourMapTemperatureMetOffice

def hexToRgb(hexColour):
  return tuple(int(hexColour[i:i+2], 16) for i in (0, 2, 4))

def celciusToColour(celcius):
  return colourMapTemperature[celcius + 5]

def windSpeedToColour(windSpeed):
  return colourMapWindSpeed[windSpeed]

while True:
  try:
    n = requests.get("https://weather-broker-cdn.api.bbci.co.uk/en/observation/rss/" + locationId)
    m = re.search('Temperature: (-?\d+)', n.text)
    print("Observed: " + m.group(1) + os.linesep)
    observedTemperature = int(m.group(1))

    m = re.search('Wind Speed: (\d+)', n.text)
    print("Wind Speed: " + m.group(1) + os.linesep)
    observedWindSpeed = int(m.group(1))

    f = requests.get("https://weather-broker-cdn.api.bbci.co.uk/en/forecast/rss/3day/" + locationId)
    m = re.findall('n>Maximum Temperature: (-?\d+)', f.text)

    # When the sun sets there is no longer a maximum forecast, just use the observed
    if(len(m) == 2):
      m.insert(0, str(observedTemperature))

    print("Day 1 Max:" + m[0] + ", Day 2 Max:" + m[1] + ", Day 3 Max:" + m[2] + os.linesep)
    forecastMaximum = [int(m[2]), int(m[1]), int(m[0])]

    m = re.findall('Minimum Temperature: (-?\d+)', f.text)
    print("Day 1 Min:" + m[0] + ", Day 2 Min:" + m[1] + ", Day 3 Min:" + m[2] + os.linesep)
    forecastMinimum = [int(m[2]), int(m[1]), int(m[0])]

    for y in range(4):
      unicorn.set_pixel(7,y,hexToRgb(windSpeedToColour(observedWindSpeed)))

    for y in range(4):
      for x in range(3,7):
        unicorn.set_pixel(x,y,hexToRgb(celciusToColour(observedTemperature)))

    for d in range(2, -1, -1):
      maxRgb = hexToRgb(celciusToColour(forecastMaximum[d]))
      unicorn.set_pixel(d,3,maxRgb)
      unicorn.set_pixel(d,2,maxRgb)
      minRgb = hexToRgb(celciusToColour(forecastMinimum[d]))
      unicorn.set_pixel(d,1,minRgb)
      unicorn.set_pixel(d,0,minRgb)

    unicorn.show()

    #Every 30 minutes
    time.sleep(1800)
  except KeyboardInterrupt:
    raise
  else:
    continue
