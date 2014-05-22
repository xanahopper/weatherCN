#!/usr/bin/env python2
#-*- coding: utf-8 -*-
# vim:fileencoding=utf-8:noet
import os
import urllib
import json
import datetime
import xml.etree.cElementTree as etree
from pprint import pprint

# 引用中国天气的城市列表
CityListXmlUrl = "http://mobile.weather.com.cn/js/citylist.xml"
WeatherUrl = "http://www.weather.com.cn/data/cityinfo/%s.html"
CurrentWeatherUrl = "http://www.weather.com.cn/data/sk/%s.html"

configFile = 'weather.conf'
cityListFile = 'cityList.xml'

version = '0.1'


def cacheCityList():
    """
    缓存城市列表，文件名为当前目录下cityList.xml。如果需要刷新，请删除该文件再调用本方法。
    本方法会在getCity第一次调用时调用。
    （一般而言，weather.com.cn的城市列表不会经常变动，如果发现获取有误可尝试更新缓存列表）
    
    返回值：无
    """
    cityFile = urllib.urlretrieve(CityListXmlUrl, cityListFile)


def getCity(cityName):
    """
    在城市列表中寻找当前城市名（中文城市名请使用unicode），第一次调用时如果未发现城市列表
    缓存，会调用cacheCityList。

    例子：
    cityId = weatherCN.getCity('shanghai')
    cityId = weatherCN.getCity(u'北京')
    cityId = weatherCN.getCity('New York')  #必然返回None啊！这是国内城市啊！

    参数： cityName 城市名称，中英文都可
    返回值：找到了城市ID，如果未找到返回None
    """
    # 刷新城市列表
    if not os.path.exists(cityListFile):
        cacheCityList()

    cityFile = open(cityListFile, 'r')
    cityXmlTree = etree.parse(cityFile)
    for node in cityXmlTree.iter():
        # d1: 中文名， d3: 英文名
        if node.tag == 'd' and (node.attrib['d2'] == cityName or node.attrib['d3'] == cityName):
            city = node.attrib
            return city['d1']
    return None


def getWeather(cityId):
    """
    根据cityId获取该城市当前的天气情况，返回一个dict，其中
    low：低温
    high:高温
    weather:天气（晴、阴、雨、雪之类的）
    ptime:发布时间
    city:城市名称
    windDirection:风向
    windStrength:风力
    temp:当前温度
    SD:未知（看不出何意）

    参数：cityId 城市Id，由getCity返回
    返回值：包含天气情况的dict数据
    """

    Weather = {}
    wUrl = WeatherUrl % cityId
    cwUrl = CurrentWeatherUrl % cityId
    # 获得城市当日温度以及天气情况
    wf = urllib.urlopen(wUrl)
    wj = json.load(wf)
    wj = wj['weatherinfo']
    Weather['low'] = wj['temp1']
    Weather['high'] = wj['temp2']
    Weather['weather'] = wj['weather']
    # 发布时间
    Weather['ptime'] = wj['ptime']

    # 获得当前温度以及风向
    wf = urllib.urlopen(cwUrl)
    wj = json.load(wf)
    wj = wj['weatherinfo']
    Weather['city'] = wj['city']
    Weather['windDirection'] = wj['WD']
    Weather['windStrength'] = wj['WS']
    Weather['temp'] = wj['temp']
    Weather['SD'] = wj['SD']
    return Weather


def outputWeather(w):
    """
    返回一个典型的天气字符串

    参数：w 由getWeather返回的天气数据
    """
    
    ows = u'%(city)s：%(temp)s\u2103 %(low)s~%(high)s %(weather)s %(windDirection)s%(windStrength)s 湿度%(SD)s 更新时间 %(ptime)s' % w
    return ows


def currentWeather(cityName=u'北京'):
    """
    获得当前某城市的天气。

    参数：cityName 城市名，中文请使用unicode（u'城市名')，英文随意
    返回值：一个典型的天气字符串。
    """
    cityId = getCity(cityName)
    return outputWeather(getWeather(cityId))


if __name__ == '__main__':
    print currentWeather()
