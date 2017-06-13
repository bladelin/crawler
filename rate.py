# encoding: utf-8
'''
[Target] Rate 匯率
[Desc]
[Type]   POST
[Auth]   Willy
'''
import urllib,urllib2
from lxml import etree
url="http://rate.bot.com.tw/Pages/UIP004/UIP004INQ1.aspx?lang=zh-TW&whom3=USD"
request = urllib2.Request(url)
request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36")
form_data={
    "__VIEWSTATE":"/wEPDwUKMTYzMjkyNTMyN2QYAwUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgkFCHZpZXcxXzk5BQd2aWV3MV82BQd2aWV3MV83BQthZnRlck9yTm90MAULYWZ0ZXJPck5vdDEFB2VudGl0eTAFB2VudGl0eTEFBlJhZGlvMQUGUmFkaW8yBQptdWx0aVRhYnMyDw9kAgFkBQltdWx0aVRhYnMPD2QCAWQe1hwVb2AvalmtKQ47HwX76pEgXQ==",
    "__VIEWSTATEGENERATOR":"FD8244EC",
    "__EVENTVALIDATION":"/wEdABSIS1WeSk0rJWNaD+HBnyYTJw9PGITp0ywlPhA3aHhu3TaBFAUjKbMo2XSEKAXRcSC5iC+b670aPnITdCK2Jr9Zk5Cg4cLff1kDXgeFYrljYHDMdP+JDfquB0JCH5rejrIlmceTax3eakf7mdzHHDphBxhSpp4StHYXMLbD9Nj5gZlDrgbtpq8GvDzzk0wyhCvdRuTH7Sxk1GMzHzh1lPEbXFWqB4QKYjYFCvvDmQ0Nk8kCKvP8wJMd+eRMYfuMWi+1FOdQUPWSmg25KZOg40zNu2EHN3PD5BlA6GEicQGKPM34O/GfAV4V4n0wgFZHr3dxHgg4R4S10gWK3akGiboUYiGjaoUF/VAZ1kOVcBiEElGB8JqnIiIqPXJZlA9AXX/lsOoPW3rv9if9K2mThiNhi7kLJnpB8B/U17unWNWfoQ0IMDszVAXFnCqunXccpyXCN6dT",
    "view":1,
    "lang":"zh-TW",
    "term":6,
    "year":2016,
    "month":03,
    "day":01,
    "afterOrNot":0,
    "whom1":"USD",
    "whom2":"",
    "entity":1,
    "Button1":"查詢",
    "lang":"zh-TW",
    "term2":1,
    "year2":2016,
    "month2":03,
    "day2":18,
}
form_data = urllib.urlencode(form_data)

response = urllib2.urlopen(request,data=form_data)
html = response.read()

page = etree.HTML(html)

for i in page.xpath(u"//td[@class='title' or @class='decimal']/a/text()|//td[@class='title' or @class='decimal']/text()"):
   print i