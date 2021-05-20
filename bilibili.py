import requests, json, os, subprocess
from lxml import etree

audioPath = './audio/'
videoPath = './video/'
imgPath = './img/'
mergePath = './merge/'

if not os.path.isdir(audioPath):
    os.mkdir(audioPath)
if not os.path.isdir(videoPath):
    os.mkdir(videoPath)
if not os.path.isdir(imgPath):
    os.mkdir(imgPath)
if not os.path.isdir(mergePath):
    os.mkdir(mergePath)

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'referer': 'https://www.bilibili.com/',
    'cookie': ''
}


# 解析bilibili html的bv地址
def getBilibiliBvUrls(file):
    bvUrls = []
    techHtml = etree.parse(file, etree.HTMLParser())
    # groom-module
    groom_modules = techHtml.xpath('//div[@class="groom-module"]/a/@href')
    # spread-module
    spread_modules = techHtml.xpath('//div[@class="spread-module"]/a/@href')
    # rank-item h
    rank_item_highlight = techHtml.xpath('//li[contains(@class,"highlight")]/a/@href')
    # rank-item
    rank_items = techHtml.xpath('//li[@class="rank-item"]/a/@href')
    bvUrls.extend(groom_modules)
    bvUrls.extend(spread_modules)
    bvUrls.extend(rank_item_highlight)
    bvUrls.extend(rank_items)
    return bvUrls


# 获取bilibili   标题、视频url、音频url、图片url
# bvurls  list
def getBilibiliHtmlUrl(bvurls, num):
    videos = []
    count = 1
    for bvurl in bvurls:
        if count >= num:
            break
        res = requests.get(url=bvurl, headers=headers)
        html = etree.HTML(res.text)
        data = html.xpath('/html/head/script[5]/text()')
        data_json = json.loads(data[0][20:])
        videourl = data_json['data']['dash']['video'][0]['baseUrl']
        audiourl = data_json['data']['dash']['audio'][0]['baseUrl']
        title = html.xpath('/html/head/meta[@itemprop="name"]/@content')[0][:-26]
        imgurl = html.xpath('/html/head/meta[@itemprop="image"]/@content')[0]
        video = {
            'title': title,
            'url': bvurl,
            'videourl': videourl,
            'audiourl': audiourl,
            'imgurl': imgurl
        }
        print(video)
        count += 1
        videos.append(video)
    return videos


# 0 0 0  不下载
# 0 0 1  下载图片
# 0 1 0  下载音频
# 1 0 0  下载视频
def downloadBvVideo(url):
    if url.find('?') > 0:
        url = url.split('?')[0]
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    # data = html.xpath('/html/head/script[5]/text()')
    datas = html.xpath('//script[not(@type) and not(@charset) and not(@src)]/text()')
    data = ''
    for temp in datas:
        if temp.startswith('window.__playinfo__'):
            data = temp
            break
    if data == '':
        print('解析失败！')
    data_json = json.loads(data[20:])
    videourl = data_json['data']['dash']['video'][0]['baseUrl']
    audiourl = data_json['data']['dash']['audio'][0]['baseUrl']
    title = html.xpath('/html/head/meta[@itemprop="name"]/@content')[0][:-26]
    videoname = url.split('/')[-1] + '.mp4'
    resaudio = requests.get(url=audiourl, headers=headers)
    save(videoname, resaudio.content, 'audio')
    resvideo = requests.get(url=videourl, headers=headers)
    save(videoname, resvideo.content, 'video')
    return videoname, title


# 下载电影
# 记得更新cookie
def downloadMovie(url, cookie):
    headers['cookie'] = cookie
    if url.find('?') > 0:
        url = url.split('?')[0]
    res = requests.get(url=url, headers=headers)
    html = etree.HTML(res.text)
    datas = html.xpath('//script[not(@type) and not(@charset) and not(@src)]/text()')
    data = ''
    for temp in datas:
        if temp.startswith('window.__playinfo__'):
            data = temp
            break
    if data == '':
        print('解析失败！')
    data_json = json.loads(data[20:])
    videoname = url.split('/')[-1] + '.mp4'
    videourl = data_json['data']['dash']['video'][0]['baseUrl']
    audiourl = data_json['data']['dash']['audio'][0]['baseUrl']
    resaudio = requests.get(url=audiourl, headers=headers)
    save(videoname, resaudio.content, 'audio')
    resvideo = requests.get(url=videourl, headers=headers)
    save(videoname, resvideo.content, 'video')
    return videoname, url


# 0 0 0  不下载
# 0 0 1  下载图片
# 0 1 0  下载音频
# 1 0 0  下载视频
def download(type, videos):
    for data in videos:
        if type & 1 == 1:
            resimg = requests.get(url=data['imgurl'], headers=headers)
            save(data['url'].split('/')[-1] + data['imgurl'][-4:], resimg.content, 'img')
        if type & 2 == 2:
            resaudio = requests.get(url=data['audiourl'], headers=headers)
            save(data['url'].split('/')[-1] + '.mp4', resaudio.content, 'audio')
        if type & 4 == 4:
            resvideo = requests.get(url=data['videourl'], headers=headers)
            save(data['url'].split('/')[-1] + '.mp4', resvideo.content, 'video')


# 保存视频
def save(name, content, prefix):
    with open('./' + prefix + '/' + name, 'wb') as f:
        f.write(content)
        f.flush()


# 合成视频
def merge(name, title):
    command = 'ffmpeg -i %s -i %s -c copy %s.mp4 -y -loglevel quiet' % (
        videoPath + name, audioPath + name, mergePath + title)
    print(command)
    subprocess.Popen(command, shell=True)
