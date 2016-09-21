# coding=utf-8
import urllib
import re
import time

#获取网页中的所有图片url
def parseTarget(url):
    content=urllib.urlopen(url).read()#以源码方式打开url
    #print(content)
    #pattern = r'src="(.*?\.jpg)" '#根据网页图片模式更改正则式
    pattern = r'src="(.*\.jpg)" '
    imglist = re.findall(pattern,content)#在源码中寻找pattern，将结果列表
    return imglist

#下载urls中的图片
def downloadURL(urls):
    """
    urls: 需要下载的url列表
    dirpath: 下载的本地路径
    """
    i = 0
    for url in urls:
        if len(url)>0:
            urllib.urlretrieve(url, './images/%05d.jpg'%i)#下载url中的图片到本地dirpath
            print('now downloading: '+url)
            i += 1


urls = []#需要下载的图片地址列表
# for i in range(1,3):
#     http_url = "http://www.ivsky.com/tupian/ziranfengguang/index_%s" % str(i)+".html"
#     try:
#         urls.extend(parseTarget(http_url))
#     except:
#         break
http_url = "http://www.ivsky.com/tupian/ziranfengguang/index_1.html"
urls.extend(parseTarget(http_url))
print(urls)
time1 = time.time()
downloadURL(urls)
time2 = time.time()
print u'耗时:' + str(time2 - time1)
