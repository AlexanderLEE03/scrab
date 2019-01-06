# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import os
import json
import codecs
class WeatherPipeline(object):
    filepath = 'G://tempfile//weather'
    os.chdir(filepath)
    filename = 'suzhou' + '_'
    def process_item(self, item, spider):
        print(os.getcwd())

        with open(self.filename + item['date']+'.png','wb+') as f:
            f.write(requests.get(item['img']).content)
        # print(item)
        return item

class W2json(object):
    filepath = 'G://tempfile//weather'
    os.chdir(filepath)
    # filename = 'suzhou.json'
    def process_item(self, item, spider):
        with codecs.open('suzhou.json' ,'a+')as f:
            line = json.dumps(dict(item),ensure_ascii=False)+'\n'
            f.write(line)
        return item
