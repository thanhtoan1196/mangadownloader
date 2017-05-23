import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import json
from manga_downloader import MangaDownloader

class Manga24h(MangaDownloader):

  def _parsing_main_page(self):
    print "parsing"
    try:
      response = requests.get(self.mangaURL)
    except requests.exceptions.RequestException as e:
      print "Gotta error :" + str(e)
      return

    parsed_html = BeautifulSoup(response.text, 'html.parser')
    option_select = parsed_html.find("select", class_ = "form-control")
    if option_select is not None:
      parsed_chapters = option_select.find_all("option",limit=2000)
      for chapter in parsed_chapters:
        for attr,val in chapter.attrs.iteritems():
          if attr == 'value':
            link = val
            if "http://manga24h.com/" not in link:
              link = "http://manga24h.com/" + link

            self.chapterList.append(link)
    else:
      print "Cannot find manga list"
    self.chapterList = list(reversed(self.chapterList))
    return

  def _parsing_chapter_page(self,chapterURL):
    self.imageList = []
    try:
      response = requests.get(chapterURL)
    except requests.exceptions.RequestException as e:
      print "Gotta error :" + str(e)
      return

    parsed_html = BeautifulSoup(response.text, 'html.parser')
    data_img = parsed_html.find("div",{"id":"chapcontent"}).find_all("div",{"class":"text-center img_episode"})
    for div_image in data_img:
      image = div_image.find("img")
      self.imageList.append(image['src'])
    return
