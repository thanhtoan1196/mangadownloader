 # -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import json
import time

URLfeed = 'https://www.chotot.com/tp-ho-chi-minh/mua-ban-bat-dong-san'
LASTLink = 'nothing'
MAXprice = 1500000000


def getting_feed_and_parse():
  url = URLfeed
  response = requests.get(url)
  parsed_html = BeautifulSoup(response.text,'html.parser')

  data = parsed_html.find_all("div", class_ = 'chotot-list-row')
  return data

def parsing_data(data,lastlink):
  newlastlink = []
  for parse_item in data:
    strPrice =parse_item.find("div", class_ = 'ad-price').text
    price = convert_price(strPrice)
    link = parse_item.find("a", class_ = 'ad-subject')
    category = parse_item.find("a", class_ = 'ad-category-region').text

    if (link['href'] in lastlink):
      break

    newlastlink.append(link['href'])

    if price < MAXprice and filter_category(category):
      print category
      print "%s --------- %s" % (link['title'], strPrice)
      print link['href']
      print "------------------------"
      print ""
      time.sleep(5)

  if len(newlastlink) == 0:
    return lastlink

  return newlastlink

def filter_category(category):
  filter = [u'Đất', u'Nhà ở']
  for item in filter:
    if item in category:
      return True
      break
  return False

def convert_price(strPrice):
  strPrice = strPrice.replace(u' đ',"")
  strPrice = strPrice.replace(".","")
  try:
    price = int(strPrice)
  except:
    price = 0
  return price


if __name__ == '__main__':
  lastlink = []
  while True:
    try:
      before = len(lastlink)
      data = getting_feed_and_parse()
      lastlink = parsing_data(data,lastlink)
      if len(lastlink) == before:
        print "nothing new"

      time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
      print "STOPPED"
      break
  pass
