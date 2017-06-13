# encoding: utf-8
'''
[Target] TravelAdvisor
[Type]   GET
[Auth]   Byron.chen
'''

import urllib2
from lxml import etree

# 定義網站路徑
tripadvisorPath = "https://www.tripadvisor.com.tw"

# function 取得頁面內容產生 xml 結構
def getUrlXml( url ):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    html = response.read()
    page = etree.HTML(html)
    return page

page = getUrlXml(tripadvisorPath+"/Tourism-g297907-Hualien-Vacations.html")

# 讀取跟花蓮有關的項目
for li in page.xpath(u"//div[contains(@class, 'navLinks')]/ul/li"):
    a = li.xpath(u"a")[0]
    # 取得項目名稱
    name = a.xpath(u"span[contains(@class, 'typeName')]")[0].text
    # 取得跟觀光有關的
    if name == u"觀光":
        # 取得觀光路徑
        href =  a.xpath(u"@href")[0]
        print tripadvisorPath + href
        # 取得跟觀光有關的訊息
        page2 = getUrlXml(tripadvisorPath + href)
        FILTERED_LIST = page2.xpath(u"//div[@id='FILTERED_LIST']/div")
        for div in FILTERED_LIST:
            # 節點不是廣告跟 分頁
            if not (div.xpath(u"contains(@class, 'inlineAd')") or div.xpath(u"contains(@class, 'al_border')") ):
                # 印出觀光景點的名字
                print div.xpath(u"div[contains(@class, 'element_wrap')]//div[contains(@class, 'property_title')]/a")[0].text
                # 印出觀光景點的下一頁網址
                print tripadvisorPath + div.xpath(u"div[contains(@class, 'element_wrap')]//div[contains(@class, 'property_title')]/a")[0].xpath("@href")[0]