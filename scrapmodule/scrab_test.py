from scrapy.selector import Selector

body = open('tt.xml','r').read()

# print(body)
title1 = Selector(text= body).xpath('//ul[@class = "txt txt2"/li]').extract()
# print(title1)
