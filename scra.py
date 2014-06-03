#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import json
import sys
from time import strftime

count = 0

from time import strftime
from random import randint

class Scraper:
    def freekaamaal(self):
        global count
        url='http://freekaamaal.com/coupons/'
        print 'Now scraping %s '%(url)
        arr =[]
        soup = BeautifulSoup( urllib2.urlopen(url).read() )

        for j in soup.find_all('div',{'class' : 'coupon abstract'} ):
            dict = {}
            name = j.find('a',class_="thumb").get('href')
            print name
            name = name.split('/')[-2] #splitting via /
            name = name.split('.')[0] #splitting via . [returns bad url for dominos.co.in]
            code = j.find('div',class_="crux").findNext('strong').get_text()
            description = j.find('div',class_="crux").findNext('p').get_text().strip()
            value = 0
            dict = return_dict(name,code,description,value)
            arr.append(dict)
            count =count +1
        return arr

    def indiafreestuff(self):
        global count
        url='http://coupons.indiafreestuff.in/'
        arr =[]
        print 'Now scraping %s \n'%(url)
        soup = BeautifulSoup( urllib2.urlopen(url).read() )
        featured = soup.find('div',{'id' : 'topCoupons'})
        for j in soup.find_all('div',{'class' : 'coupon abstract'} ):
            dict = {}
            name = j.find('a',class_="thumb").get('href')
            print name
            name = name.split('/')[-2]
            code = j.find('div',class_="crux").findNext('strong').get_text()
            description = j.find('div',class_="crux").findNext('p').get_text().strip()
            value = 1
            dict = return_dict(name,code,description,value)
            arr.append(dict)
            count = count +1

        return arr

    def desidime(self):
        global count
        url='http://www.desidime.com/coupons'
        print 'Now scraping %s \n'%(url)

        dict = {}
        arr = []
        feat_arr = []
        soup = BeautifulSoup( urllib2.urlopen(url).read() )
        featured = soup.find('div',{'id' : 'topCoupons'})
        list_norm = soup.find('div',{'class' : 'active_coupons_text'}).findNext('ul')
        list_feat = soup.find('div',{'class' : 'coupon_headline'}).findNext('ul')

        def scrape_dime(list,value):
            global count
            arr =[]
            for j in list:
                dict ={}
                try:
                    name = j.find('div',{'class' : 'coupon_img'}).find('a').get('href')
                    name = name.split('/')[-1].split('-')[0]
                    description = j.find('div',{'class' : 'coupon_text'}).find('a').get_text()
                    code = j.find('div',{'class' : 'code_area'}).find('a').get_text()
                    value = 0
                    dict = return_dict(name,code,description,value)
                    arr.append(dict)
                    count = count +1
                except Exception as e: 
                    pass
                    #print e
            return arr

        return  scrape_dime(list_feat,1) + scrape_dime(list_norm,0) 
            
def return_dict(name,code,description,value):
    global count
    dict = {}
    dict['url'] = gen_url(name)
    dict['favicon'] =gen_favicon(name)
    dict['name'] = name
    dict['code'] = code
    dict['description'] = description
    dict['value'] = value
    try:
        print '#%d  %s : %s : %s'%(count,name,code,description)
    except:
        pass
    return dict



def gen_url(name):
    url = 'http://www.%s.com'%(name)
    #FUCK ALL OF THIS
    return url
    url2 = 'http://www.%s.in'%(name)
    try:
        f = urllib2.urlopen(urllib2.Request(url))
        return url
    except Exception as e:
        print 'ERROR in gen_ulr : '
        print e
        try: 
            f = urllib2.urlopen(urllib2.Request(url2))
            return url2
        except:
            return url

def gen_favicon(name):
    return 'NULL'
    url = gen_url(name)
    try:
        soup = BeautifulSoup( urllib2.urlopen(url).read() )
        link = soup.find('link',{'rel' : 'shortcut icon'}).get('href')
        return link
    except Exception as e:
        print 'ERROR in gen_favicon '
        print e
        return 'NULL'

def is_good(item):
    for key,val in item.iteritems():
        if val == '' or 'Click to see code' in val: 
            return False 
    
    return True

def main():
    scrape = Scraper()
    arr1 = scrape.freekaamaal()
    arr2 = scrape.indiafreestuff()
    arr3 = scrape.desidime()
    arr = arr1 + arr2 + arr3
    
    # filtering the array according to is_good() function
    final_arr = filter(lambda item: is_good(item), arr)    
    #final_arr = [item for item in arr if is_good(item)]
    
    #Appending a dummy object at index 0 in final_arr
    final_arr.insert(0,{'dummy':'%d coupons scraped: time %s'%( len(final_arr),strftime("%Y-%m-%d %H:%M:%S")) } )
    final_arr.insert(randint(3,len(final_arr)-2),{"code": "sauravtom.com", "description": "Upto 25% discount on new domains", "url": "http://www.bigrock.com/?coupon=sauravtom.com", "value": 0, "favicon": "NULL", "name": "bigrock"})
    final_arr.insert(randint(3,len(final_arr)-2),{"code": "championswimmer.in", "description": "Upto 25% discount on new domains", "url": "http://www.bigrock.com/?coupon=championswimmer.in", "value": 0, "favicon": "NULL", "name": "bigrock"})

    # writing the final_arr to json file
    with open("/home/sauravtom/public_html/coupon.txt", "w") as f:
        f.write(json.dumps(final_arr))

if __name__ == '__main__':
    main()
    #print gen_favicon('flipkart')

