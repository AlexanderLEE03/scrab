import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
myencoding = None
def getHtml(url):
    try:
        r = requests.get(url, timeout=30)
        print(r.status_code)
        # 如果状态码不是200 则应发HTTOError异常
        r.raise_for_status()
        '''
        网页加密方式： ISO-8859-1 
        iso8859-1是单字节编码，而utf8是定长编码，从utf8转化成iso8859-1相当于是高精度转化成低精度，造成精度丢失，所以不可逆。
        而gbk是不定长编码，英文数字的字符编码规则跟iso8859-1是一样的
        '''

        print('网页加密方式：', r.encoding)
        # 设置正确的编码方式
        r.encoding = 'gbk'
        # r.encoding = r.apparent_encoding
        print('加密方式：',r.encoding)
        myencoding = r.encoding

        return r.text
    except:

        return "Something Wrong!"

def getcontent(url,filepath):
    comments = []
    html = getHtml(url)
    # soup = BeautifulSoup(html, 'lxml')
    #在爬虫爬取网页的时候只爬取到部分内容，后来查到原因是因为爬取的html文件是不规范的html，导致不同的html parser的分析结果不一样。
    soup = BeautifulSoup(html, 'html.parser')
    movie_list = soup.find('ul', class_ = 'picList clearfix')
    movies = movie_list.find_all('li')
    print(len(movies))

    baseurl = 'http:'
    for li in movies:
        comment = {}
        try:
            comment['title'] = li.find('span',class_ = 'sTit').a.text
            comment['img'] = baseurl+ li.find('img')['src']
            title = comment['title']
            get_pic_from_url(comment['img'],title.replace(':','：'),filepath)
            # pic_content = requests.get(comment['img'], stream=True).content
            # print(pic_content)
            comment['link'] =baseurl+ li.find('a',class_ = 'aPlayBtn')['href']
            namelist = li.find('p',class_ = 'pActor')
            names = namelist.find_all('a', attrs = {'target': '_blank'})
            actor = []
            for name in names:
                actor.append(name['title'])

            comment['name'] = actor
            comments.append(comment)

        except:
            print('Resolution failure')
            print(comment)

    return comments

def get_pic_from_url(url,filename,path):
    pic_content = requests.get(url,stream = True).content
    movie = os.path.join(path,filename)
    movie = movie+'.jpg'
    print(movie)
    with open(movie,'wb+') as f:
        f.write(pic_content)
    f.close()

def Out2File(comments):
    print('统计开始')
    with open('statistics.txt', 'wb+') as f:
        for comment in comments:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(comment['title'],
                 comment['link'], comment['name'], comment['time'], comment['replyNum']).encode('utf-8'))
    f.close()
    print('统计完成')

def main(url):
    print('网页信息下载完成，开始筛选信息。。。。')
    filepath = 'G://tempfile//movie'
    content = getcontent(url,filepath)

    df = pd.DataFrame(content)
    df.to_csv('movie.csv')
    print(df.info())

    print('所有信息已经保存完毕！')




if __name__ == '__main__':
    # # filename = 'url.txt'
    url = 'http://dianying.2345.com/top/'
    main(url)

    # filepath = 'G://tempfile//movie'
    # url ='http://imgwx1.2345.com/dypcimg/img/2/66/sup199753_223x310.jpg?1533805777'
    # filename = '精灵旅社3:疯狂假期'
    # filename = filename.replace(':','：')
    # print(filename)
    # get_pic_from_url(url,filename,filepath)

