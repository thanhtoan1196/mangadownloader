import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import json
from manga_downloader import MangaDownloader

class TruyenTranhTuan(MangaDownloader):

	def _parsing_main_page(self):
		print "parsing"
		try:
			response = requests.get(self.mangaURL)
		except requests.exceptions.RequestException as e:
			print "Gotta error :" + str(e)
			return

		parsed_html = BeautifulSoup(response.text, 'html.parser')
		chapter_list = parsed_html.find(id = 'manga-chapter')
		if chapter_list is not None:
			parsed_chapters = chapter_list.find_all("span",class_='chapter-name')
			for chapter in parsed_chapters:
				link = chapter.a['href']
				if "http://truyentranhtuan.com/" not in link:
					link = "http://truyentranhtuan.com/" + link
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
		scripts = parsed_html.find_all('script')
		main_script = ""
		for script in scripts:
			if "slides_page_path" in script.text:
				main_script = script.text
				break

		data_img = re.search(r"var slides_page_path = \[(.*)\]", main_script).group(1).split(",")
		for img_str in data_img:
			image = img_str.strip('"')
			self.imageList.append(image)
		self.imageList.sort()

		return
