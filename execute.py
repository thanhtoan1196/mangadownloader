from manga24h import Manga24h

if __name__ == '__main__':
	url = "http://manga24h.me/Samurai-Deeper-Kyo.htm"

	downloader = Manga24h(url,"log/downloaded_chapter.log","log/downloaded_image.log","log/downloaded_failure_image.log")

	downloader.start_download()

	pass
