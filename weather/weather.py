import requests
import pandas as pd
import csv

"""
    @project: 爬取天气预报数据
    @author: ChenchenJT
"""

def getweather():
    # 利用pandas库进行数据清洗
    df = pd.read_csv('china-city-list.csv')
    for cityID in df.get('City_ID'):
        cityID= str(cityID)
        url='http://wthrcdn.etouch.cn/weather_mini?citykey='+cityID
        response=requests.get(url)
        response.encoding='utf8'
        dic=response.json()
        cityName = dic['data']['city']
        for item in dic['data']['forecast']:
            yield {
                '城市编码': cityID,
                '城市名称': cityName,
                '时间': item['date'],
                '天气': item['type'],
                '最高温度': item['high'],
                '最低温度': item['low']
            }

def savetocsv(weather):
    """
    保存到csv文件
    :param: 天气信息
    :return:
    """
    with open('weather.csv', 'a+', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['城市编码', '城市名称', '时间', '天气', '最高温度', '最低温度' ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(weather)

if __name__ == '__main__':
    items=getweather()
    for item in items:
        print(item)
        savetocsv(item)
