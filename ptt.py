# encoding: utf-8
'''
[Target] PTT
[Desc]   練習cookie儲存及設定cookie值，這邊用來skip PTT 18歲的選擇限制
[Type]   POST
[Auth]   Jun.lin
'''
import urllib2
import cookielib
from lxml import etree

filename = 'cookie.txt'
cookie = cookielib.MozillaCookieJar(filename)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)
opener.addheaders.append(('Cookie', 'over18=1'))

cookie.save(ignore_discard=True, ignore_expires=True)

request = urllib2.Request("http://www.ptt.cc/bbs/Job/index.html")
response = opener.open(request)

html = response.read()

page = etree.HTML(html)
count = 0

for i in page.xpath(u"//div[@class='r-ent']/div[@class='title']/a"):
    print i.text
