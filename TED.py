import requests, json, re
from lxml import etree


# 获取TED的网址
def getTed():
    url = 'https://open.163.com/ted/'
    res = requests.get(url=url)
    html = etree.HTML(res.text)
    banner = html.xpath('//script[@type="text/javascript"]/text()')[3]
    print(banner)
    result = re.search('', banner)
    print(result)


if __name__ == '__main__':
    getTed()
    'style="background-image: url("https://nimg.ws.126.net/?url=http://open-image.ws.126.net/image/snapshot_movie/2018/8/Q/S/MDPBVMKQS.jpg&thumbnail=860x483&quality=95&type=jpg");"'
