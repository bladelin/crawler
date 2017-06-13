# encoding: utf-8
import urllib,urllib2
import os.path
import md5
import TWS_all_station
from lxml import etree
from collections import Counter

'''
 取得高鐵時刻表
 @param [string] date
 @param [int]    depart
 @param [int]    arrive
 @return avoid display string
'''
def getTHS(date, depart, arrive):

    url ="http://www.thsrc.com.tw/tw/TimeTable/SearchResult"
    request = urllib2.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36")

    form_data = {
        "StartStation":_THS[depart],
        "EndStation":_THS[arrive],
        "SearchDate":date,
        "SearchTime":"09:00",
        "SearchWay":"DepartureInMandarin",
        "RestTime":"",
        "EarlyOrLater":""
    }

    form_data = urllib.urlencode(form_data)
    response = urllib2.urlopen(request,data=form_data)
    html = response.read()

    page = etree.HTML(html)

    i=0
    my_list =[]
    for tbl in page.xpath(u"//table[@class='touch_table']"):
        tds = tbl.xpath(u".//tr/td")

        sub_list = []
        sub_list.append(tds[0].xpath('.//a')[0].text)
        sub_list.append(tds[1].text)
        sub_list.append(tds[2].text)
        if tds[3].text :
            sub_list.append(tds[3].text)
        my_list.append(sub_list)

    for i in my_list:
        print '\t'.join(i)

'''
 取得台鐵時刻表
 @param [string] date
 @param [int]    depart
 @param [int]    arrive
 @return avoid display string
'''
def getTWT(date, depart, arrive):

    url ="http://twtraffic.tra.gov.tw/twrail/SearchResult.aspx"
    form_data = {
        'searchtype':'0',
        'searchdate': date,
        'fromcity':'0',
        'tocity':'10',
        'fromstation':_TWT[depart],
        'tostation':_TWT[arrive],
        'trainclass':'2',
        'timetype':'1',
        'fromtime':'0000',
        'totime':'2359'
    }

    request = urllib2.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36")

    form_data = urllib.urlencode(form_data)
    request = url + "?" + form_data

    m = md5.new()
    m.update(request)
    m.digest()
    md5_url =  m.hexdigest()
    tmp_file = "/tmp/" + md5_url + ".html"
    if os.path.isfile(tmp_file) :
        with open(tmp_file, 'r') as content_file:
            html = content_file.read()
    else :
        response = urllib2.urlopen(request)
        html = response.read()
        file_out = file(tmp_file,'w')
        file_out.write(html)
        file_out.close()


    page = etree.HTML(html)
    i=0

    my_list =[]
    for tr in page.xpath(u"//tr[@class='Grid_Row']"):
        detail =[]
        if i > 0:
            # Debug way
            # innerHTML = etree.tostring(tr, pretty_print=True,encoding='UTF-8')
            # print innerHTML
            # exit(1)

            # 非常要注意，因為回傳為陣列，最後還是得加個[0]，即便只有一個
            detail.append(tr[0].xpath(u".//font/div/span")[0].text)
            detail.append(tr[1].xpath(u".//a")[0].text)
            detail.append(tr[2][0].text)
            detail.append(tr[3][0].text)
            detail.append(tr[4][0].text)
            detail.append(tr[5][0].text)
            detail.append(tr[6][0].text)
            my_list.append(detail)
        i=i+1

    #print my_list
    for i in my_list:
        print '\t'.join(i)

'''
 Main
'''
if __name__ == "__main__":
    date = '2017/03/31'
    depart = '板橋'
    arrive = '豐原'

    _THS = TWS_all_station.THS_station
    _TWT = TWS_all_station.TWT_station

    if not _THS.has_key(depart) or not _THS.has_key(arrive):
        print '高鐵 查無此站資料 [日期] '+date+' [出發] '+ depart + ' [到達] '+arrive
    else:
        print '高鐵 時刻表 '+ date + ' departures: '+ depart + ' arrivals:' + arrive
        getTHS( date, depart, arrive )

    if not _TWT.has_key(depart) or not _TWT.has_key(arrive):
        print '台鐵 查無此站資料 [日期] '+date+' [出發] '+ depart + ' [到達] '+arrive
    else:
        print '台鐵 時刻表 '+ date + ' departures: '+ depart + ' arrivals:' + arrive
        getTWT( date, depart, arrive )



