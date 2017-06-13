# encoding=utf8
import MySQLdb
import requests
import time
import base64
import random
import datetime
import os
import wget
import json
import re
import pytz
#import utility
from lxml import etree
from urlparse import urlparse, parse_qs

_SOURCE = "Romhustler"
_URL = "http://romhustler.net";

def get_decode_url(url):
    try:
        resp = requests.get(url)
        page = etree.HTML(resp.text)
        item = page.xpath("//a[@class='dlpage1 download_link']/@href")[0].split("/")[3];
        num  = page.xpath("//a[@class='dlpage1 download_link']/@href")[0].split("/")[2];
        raw = base64.b64decode(base64.b64decode(item))
        raw = raw.replace('download_page', 'final_download_link')
        filelink = _URL+'/file/'+num+'/'+base64.b64encode(base64.b64encode(raw))
        return filelink
    except:
        return false

def get_article(pIndex, url, machine):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    page = etree.HTML(resp.text)
    index = 1
    for article in page.xpath("//div[@class='title']/a"):
        title = article.text
        link = article.xpath("./@href")[0].strip();
        item_url = _URL+link
        print '#'+ str((pIndex*100)+index) +' [enter]: '+title+' [link]: '+item_url
        filelink = get_decode_url(item_url)

        if filelink:
            save(title, machine, filelink)
        index +=1

def save(name, machine, url) :
    name = name.replace(' ', '-')
    name = re.sub('[^A-Za-z0-9]+', '', name)

    savename = machine+'/'+ name +'.zip'

    if os.path.isfile(savename):
        print "file exists"
    else :
        print "download"
        os.system('wget '+url+' -q -O ./'+machine+'/'+ name +'.zip');

def get_list(list_url, machine):
    resp = requests.get(list_url)
    resp.encoding = "utf-8"
    page = etree.HTML(resp.text)

    # get last page
    page = page.xpath("//div[@class='pagi_nav']/span/text()")[-1];
    max_page = page.split('of')[1].split(',')[0];

    print "%s 大約有 : %d筆 " %(machine, int(max_page)*100)

    print '[Machine]: '+machine+' [Total Page]: '+max_page

    pIndex = 0
    for p in range(1,int(max_page)+1):
        if p > 1 :
            url = list_url+'/page:'+str(p)
        else :
            url = list_url
        get_article(pIndex, url, machine)
        pIndex +=1

def main():
    url = _URL+"/roms/%s";

    machines = ["nes"]
    for machine in machines:
        get_list(url % (machine), machine)


import sys
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
