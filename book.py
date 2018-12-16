import requests
from bs4 import BeautifulSoup
import pandas as pd
import string
import os,sys
myencoding = None
def get_Html(url):
    try:
        r = requests.get(url, timeout=30)
        print(r.status_code)
        # 如果状态码不是200 则应发HTTOError异常
        r.raise_for_status()
        # 设置正确的编码方式
        r.encoding = 'utf-8'
        # r.encoding = r.apparent_encoding
        print('加密方式：',r.encoding)
        myencoding = r.encoding
        return r.text
    except:

        return "Something Wrong!"

def get_content(url):
    comments = []
    html = get_Html(url)
    soup = BeautifulSoup(html, 'lxml')

    categorylist = soup.find_all('div', class_ ='index_toplist mright mbottom')
    historylist = soup.find_all('div', class_ = 'index_toplist mbottom')


    for cate in categorylist:
        type= cate.find('div',class_ = 'toptab').span.string
        generallist = cate.find(style = 'display: block;')
        booklist = generallist.find_all('li')
        for book in booklist:
            comment = {}
            try:
                comment['type'] = type
                comment['name'] = book.a['title']
                comment['link'] = 'https://www.qu.la'+ book.a['href']
                comments.append(comment)

            except:
                print('Resolution failure')
                print(comment)
                continue

    for cate in historylist:
        type= cate.find('div',class_ = 'toptab').span.string
        generallist = cate.find(style = 'display: block;')
        booklist = generallist.find_all('li')
        for book in booklist:
            comment = {}
            try:
                comment['type'] = type
                comment['name'] = book.a['title']
                comment['link'] = 'https://www.qu.la'+ book.a['href']
                comments.append(comment)

            except:
                print('Resolution failure')
                print(comment)
                continue

    return comments

# def Out2File(comments):
#     print('统计开始')
#     with open('statistics.txt', 'wb+') as f:
#         for comment in comments:
#             f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(comment['title'],
#                  comment['link'], comment['name'], comment['time'], comment['replyNum']).encode('utf-8'))
#     f.close()
#     print('统计完成')

def get_text_url(url):
    comments = []
    html = get_Html(url)
    soup = BeautifulSoup(html, 'lxml')

    chapter_list = soup.find_all('dd')
    for chapter in chapter_list:
        comment = {}
        try:
            text = chapter.a.text.strip(string.punctuation)
            sptext = text.split(' ')
            comment['num'] = sptext[0]
            comment['chapter'] = sptext[1]
            comment['url'] = 'https://www.qu.la' + chapter.a['href']
            comments.append(comment)
        except:
            print('Resolution failure')
            print(comment)
            continue
    return comments


def main(url):
    content = get_content(url)
    df = pd.DataFrame(content)
    df.to_csv('book.csv')
    print(df.info())
    # Out2File(content)
    print('所有信息已经保存完毕！')

def main_text(url,textname):
    content = get_text_url(url)
    df = pd.DataFrame(content)
    path = 'G:/tempfile'
    filename = '{}.csv'.format(textname)
    df.to_csv(os.path.join(path,filename))
    print(df.info())
    print('所有信息已经保存完毕！')

def main_combine(url):
    content = get_content(url)
    for index,item in enumerate(content):
        # print(item['name'],item['link'])
        name = item['name']
        link = item['link']
        print(link, name)
        html = get_Html(link)
        # print(html)
        main_text(link,name)

if __name__ == '__main__':
    # filename = 'url.txt'
    url = 'http://www.qu.la/paihangbang/'

    # url = 'https://www.qu.la/book/4140/'
    main_combine(url)



