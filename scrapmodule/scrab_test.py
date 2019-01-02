from scrapy.selector import Selector

body = open('demo.xml','r').read()

# print(body)
title1 = Selector(text= body).xpath('//div[position()<3]/a[@href="http://www.baidu.com"]/@class').extract()
print(title1)
title2 = Selector(text= body).xpath('//body/div/span').extract()
print(title2)
title3 = Selector(text= body).xpath('//div[@class="foot"]/text()').extract()
print(title3)
title4= Selector(text= body).xpath('//body/div/span[not(@*)]').extract()
print(title4)