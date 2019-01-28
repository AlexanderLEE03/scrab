# -*- coding: utf-8 -*-
import scrapy
from weather.items import WeatherItem

class SztianqiSpider(scrapy.Spider):
    name = 'SZtianqi'
    allowed_domains = ['tianqi.com']
    start_urls = ['http://www.tianqi.com/shanghai/']

    def parse(self, response):
        items = []

        day7 = response.xpath('//div[@class="day7"]')
        week = day7.xpath('./ul[@class = "week"]/li')
        week_len = len(week)
        date = []
        day_week = []
        img = []
        for day in week:
            date.append(day.xpath('./b/text()').extract()[0])
            day_week.append(day.xpath('./span/text()').extract()[0])
            url = 'https:'+ day.xpath('./img/@src').extract()[0]
            img.append(url)

        weather = []
        weather_ul = day7.xpath('./ul[@class = "txt txt2"]/li')
        for day in weather_ul:
            weather.append(day.xpath('./text()').extract()[0])

        H_temp = []
        L_temp = []
        temp = day7.xpath('./div[@class = "zxt_shuju"]/ul/li')
        for day in temp:
            H_temp.append(day.xpath('./span/text()').extract()[0])
            L_temp.append(day.xpath('./b/text()').extract()[0])

        wind = []
        wind_ul = day7.xpath('./ul[@class ="txt"]/li')
        for day in wind_ul:
            wind.append(day.xpath('./text()').extract()[0])



        for i in range(week_len):
            item = WeatherItem()
            item['date'] = date[i]
            item['week'] = day_week[i]
            item['img'] = img[i]
            item['weather'] = weather[i]
            item['H_temperature'] = H_temp[i]
            item['L_temperature'] = L_temp[i]
            item['wind'] = wind[i]
            items.append(item)

        return items
