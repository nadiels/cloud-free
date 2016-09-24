# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:09:04 2016

@author: danieltait
"""

from bs4 import BeautifulSoup

import requests
import numpy as np

url = "http://www.mwis.org.uk/scottish-forecast/WH"
url2 = "http://www.metoffice.gov.uk/public/weather/forecast/gfhd2880r"


r  = requests.get(url)
r2 = requests.get(url2)
data = r.text
met_data = r2.text



#with open('mwis.html') as f :
#    soup = BeautifulSoup(f,'html.parser')

soup = BeautifulSoup(data,'html.parser')
met_soup = BeautifulSoup(met_data,'html.parser')

#area = "The Northwest Highlands"    
area = "West Highlands"
AREAS = [area]
labels = ["Summary for all mountain areas",
          "Headline for "+area,
          "How windy? (On the Munros)",
          "Effect of wind on you?",
          "How Wet?",
          "Cloud on the hills?",
          "Chance of cloud free Munros?",
          "Sunshine and air clarity?",
          "How Cold? (at 900m)",
          "Freezing Level"]
    
rs = soup.find_all("div", {"class": "row indentDetails"})


#<tr class="weatherTime">
#<tr class="titleWind wxContent" data-panel="show">

"""
<span class="iconTitleOnly" title="Light shower day"><i
class="icon"
data-type="wx"
title="Light shower day"
data-value="10">
"""


#<title>Stob Dearg weather forecast - Met Office</title>
def isMetOfficeForecast(soup):
    title = soup.find("title").contents[0]
    if "Met Office" in title:
        return True
    else:
        return False

def getMetOfficeSummary(soup,day=0):
    rs = soup.find_all("span",{"class" : "iconTitleOnly"})
    return str(rs[day]["title"])

def getMetOfficeData(soup):
    trs = soup.find_all("tr", {"class": "weatherTime"})
    w_rs = soup.find_all("tr", {"class": "weatherWind wxContent"})
    t_rs = soup.find_all("tr", {"class": "weatherTemp"})
    
    today_time = []; today_speed = []; today_temp = []
    times = trs[0].find_all("td")
    wspeeds = w_rs[0].find_all("i", {"data-type":"windSpeed"})
    temps = t_rs[0].find_all("i", {"data-type":"temp"})
    for i in range(len(times)):
        today_time.append(float(times[i].contents[0]))
        today_speed.append(float(wspeeds[i].contents[0]))
        today_temp.append(float(temps[i]["data-c"]))
    return today_time, today_temp, today_speed

metData = np.column_stack((today_time,today_speed))

fcast = {}
for result in rs :
    if result.find("h4") != None:
        lab = result.find("h4").contents
        summary = result.find("p").contents
        summary = str(summary[0]).strip()
        fcast[str(lab[0])] = summary
print fcast['Summary for all mountain areas']        

def validArea(area):
    if area in AREAS:
        return True
    else :
        return False

class mwisForecast:
    def __init__(self):
        self.fcast = None
    def getForecast(self,date,area):
        forecastRetrieved = False
        if not validArea(area):
            print "Please enter a valid area"
        else:
            """
            Try getting the forecast, if not available return error
            """
            self.fcast = fcast
            forecastRetrieved = False
            if forecastRetrieved :
                # Do something
                return 1
    def summary(self):
        if self.forecastRetrieved:
            print self.fcast['Summary for all mountain areas']
                
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(min_df=1)
content = ["How to format my hard disk", "Hard disk format problems"]
X = vectorizer.fit_transform(content)
vectorizer.get_feature_names()