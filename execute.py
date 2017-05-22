from manga24h import Manga24h
from truyentranhtuan import TruyenTranhTuan

if __name__ == '__main__':
	url = "http://truyentranhtuan.com/bleach/"

	downloader = TruyenTranhTuan(url,"log/downloaded_chapter.log","log/downloaded_image.log","log/downloaded_failure_image.log")

	downloader.resume_download()

	pass
