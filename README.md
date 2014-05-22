weatherCN
==========
* 获取国内城市天气情况
* 名称同时支持中英文（中文请使用unicode字符串）
* 暂时只支持Python 2

安装方法
==========

    pip install weatherCN

使用方法
==========
## 简单使用

    from weatherCN import weatherCN
    print weatherCN.currentWeather(u'上海')
    print weatherCN.currentWeather('qingdao')

## 进阶使用

    from weatherCN import weatherCN
    cityId = weatherCN.getCity('shanghai')
    weatherData = weatherCN.getWeather(cityId)

其他具体使用，请参看help。

