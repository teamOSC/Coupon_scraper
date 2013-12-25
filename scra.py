#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


class Scraper:
    def freekaamaal(self):
        url='http://freekaamaal.com/coupons/'
        arr =[]
        soup = BeautifulSoup( urllib2.urlopen(url).read() )

        for j in soup.find_all('div',{'class' : 'coupon abstract'} ):
            dict = {}
            name = j.find('a',class_="thumb").get('href')
            name = name.split('/')[-2][:-4]
            dict['name'] = name
            dict['code'] = j.find('div',class_="crux").findNext('strong').get_text()
            dict['decsription'] = j.find('div',class_="crux").findNext('p').get_text().strip()
            dict['value'] = 0
            arr.append(dict)
        return arr

    def indiafreestuff(self):
        url='http://coupons.indiafreestuff.in/'
        arr =[]
        soup = BeautifulSoup( urllib2.urlopen(url).read() )
        featured = soup.find('div',{'id' : 'topCoupons'})
        for j in soup.find_all('div',{'class' : 'coupon abstract'} ):
            dict = {}
            dict['name'] = j.find('a',class_="thumb").get('href')
            dict['code'] = j.find('div',class_="crux").findNext('strong').get_text()
            dict['description'] = j.find('div',class_="crux").findNext('p').get_text().strip()
            dict['value'] = 1
            arr.append(dict)

        return arr

    def desidime(self):
        url='http://www.desidime.com/coupons'
        dict = {}
        arr = []
        feat_arr = []
        soup = BeautifulSoup( urllib2.urlopen(url).read() )
        featured = soup.find('div',{'id' : 'topCoupons'})
        list_norm = soup.find('div',{'class' : 'active_coupons_text'}).findNext('ul')
        list_feat = soup.find('div',{'class' : 'coupon_headline'}).findNext('ul')

        def scrape_dime(list,value):
            arr =[]
            for j in list:
                dict ={}
                try:
                    name = j.find('div',{'class' : 'coupon_img'}).find('a').get('href')
                    description = j.find('div',{'class' : 'coupon_text'}).find('a').get_text()
                    code = j.find('div',{'class' : 'code_area'}).find('a').get_text()
                    name = name.split('/')[-1].split('-')[0]
                    dict['name'] = name
                    dict['code'] = code
                    dict['description'] = description
                    dict['value'] = value
                    arr.append(dict)
                    
                except: pass
            return arr

        return  scrape_dime(list_feat,1) + scrape_dime(list_norm,0) 
            


def main():
    scrape = Scraper()
    arr1 = scrape.freekaamaal()
    arr2 = scrape.indiafreestuff()
    arr3 = scrape.desidime()
    arr = arr1 + arr2 + arr3
    with open("/home/sauravtom/public_html/coupon.txt", "w") as f:
        f.write(json.dumps(arr))

if __name__ == '__main__':
    main()

