import requests
from bs4 import BeautifulSoup
import pandas as pd

myencoding = None
def getHtml(url):
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

def getcontent(url):
    comments = []
    html = getHtml(url)
    soup = BeautifulSoup(html, 'lxml')

    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    baseurl = 'http://tieba.baidu.com'
    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find('a', attrs = {'class':'j_th_tit '}).text.strip()
            comment['link'] = baseurl + li.find('a', attrs = {'class': 'j_th_tit '})['href']
            name = li.find('span', attrs = {'class': 'tb_icon_author '})
            if name is not None:
                comment['name'] = name['title'].strip()
            else:
                comment['name'] = li.find('span', attrs = {'class': 'tb_icon_author no_icon_author'})['title'].strip()
            # comment['time'] = li.find('span', attrs = {'class': 'pull-right is_show_create_time'}).text.strip()
            comment['time'] = li.find('span', class_ = 'pull-right is_show_create_time').text.strip()
            comment['replyNum'] = li.find('span', attrs= {'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)

        except:
            print('Resolution failure')
            print(comment)

    return comments

def Out2File(comments):
    print('统计开始')
    with open('statistics.txt', 'wb+') as f:
        for comment in comments:
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回复数量： {} \n'.format(comment['title'],
                 comment['link'], comment['name'], comment['time'], comment['replyNum']).encode('utf-8'))
    f.close()
    print('统计完成')

def main(crabbaseurl,count):
    urllist = []
    for i in range(0, count):
        urllist.append(crabbaseurl+'&pn='+str(50*i))
    print('网页信息下载完成，开始筛选信息。。。。')

    for url in urllist:
        content = getcontent(url)
        df = pd.DataFrame(content)
        df.to_csv('data.csv')
        print(df.info())
        # Out2File(content)
    print('所有信息已经保存完毕！')




if __name__ == '__main__':
    filename = 'url.txt'
    urltext = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'
    count = 1
    main(urltext, count)


    # html = getHtml(urltext)
    # soup = BeautifulSoup(html, 'lxml')


    # liTags = soup.find_all('div', attrs={'class': 'thread_list_bottom clearfix'})
    # liTags = soup.find_all('li', attrs={'class': 'j_thread_list clearfix'})
    # print(liTags)
    # with open('test.txt','a+') as f:
    #     for li in liTags:
    #         f.write(liTags)
    # f.close()
