import requests
from lxml import etree


# new
# title 标题
# url url
# content 新闻内容
# time 时间
# type video 视频  article 文章
def baidunews():
    types = ['guonei', 'guoji', 'mil', 'ent', 'sports', 'internet', 'tech', 'game', 'lady', 'auto', 'house']
    news = []
    baseUrl = 'https://news.baidu.com/'
    for type in types:
        res = requests.get(baseUrl + type)
        html = etree.HTML(res.text)
        nodes = html.xpath('//a[contains(@href,"baijiahao")]')
        for node in nodes:
            isVideos = False
            content = ''
            newsurl = node.get('href')
            resnews = requests.get(newsurl)
            resnews.encoding = 'utf-8'
            newshtml = etree.HTML(resnews.text)
            timenode = newshtml.xpath('//div[@class="index-module_articleSource_2dw16"]')
            if len(timenode) != 0:
                # time_ = timenode[0][0].xpath('string()') + ' ' + timenode[0][1].xpath('string()')
                # time = '2021-' + time_[-11:]
                newsnodesContent = newshtml.xpath('//div[@class="index-module_articleWrap_2Zphx"]')
                for newsnode in newsnodesContent:
                    content += newsnode.xpath('string()')
            else:
                # timenode = newshtml.xpath('//span[@data-href]')
                # if len(timenode) == 1:
                #     time = timenode[0].xpath('string()')[-16:]
                # else:
                #     time_ = newshtml.xpath('div[@class="videoinfo-playnums"]/text()')
                #     print(time_)
                newsnodesContent = newshtml.xpath('//article/p[@class="contentFont"]')
                for newsnode in newsnodesContent:
                    content += newsnode.xpath('string()')
            if content == "":
                isVideos = True
            new = {
                'title': node.xpath('string()'),
                'url': node.get('href'),
                'content': content,
                # 'time': time,
                'type': 'video' if isVideos else 'article'
            }
            print(new)
            news.append(new)
    return news


if __name__ == '__main__':
    # 获取结果
    result = baidunews()
