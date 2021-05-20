import bilibili


# 下载bv，并合成
def downloadMergeBv(url):
    videoname, title = bilibili.downloadBvVideo(url)
    bilibili.merge(videoname, title)


# 下载bv
def downloadBv(url):
    bilibili.downloadBvVideo(url)


# 下载电影，大会员使用，否则不配
def dowmloadMovie(url, cookie):
    bilibili.downloadMovie(url, cookie)


if __name__ == '__main__':
    downloadBv('https://www.bilibili.com/video/BV1df4y1p7A8?spm_id_from=333.851.b_7265636f6d6d656e64.2')
