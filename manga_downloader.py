import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import json
import zipfile
import tarfile
import sys

class MangaDownloader:
    chapterList = []
    imageList = []
    downloaded_chapter = []
    downloaded_images = []

    def __init__(self, mangaURL, downloaded_chapter_path, downloaded_image_path, failure_path):        
        self.mangaURL = mangaURL
        self.downloaded_chapter_path = downloaded_chapter_path
        self.downloaded_image_path = downloaded_image_path
        self.failure_path = failure_path
        return


    def __prepare_download_files(self,savingURL):
        if not os.path.isfile(savingURL):
            filedata = file(savingURL,"wb")
        else:
            i=0
            spliter = savingURL.split(".")
            extension = spliter[len(spliter)-1]
            newfilepath = savingURL.replace("."+extension, str(i)+"."+extension)
            
            while os.path.isfile(newfilepath):
                i+=1
                newfilepath = savingURL.replace("."+extension, str(i)+"."+extension)
                
            filedata = file(newfilepath,"wb")
        return filedata

    def __download_files(self,fileURL, savingURL):
        success = True
        try:
            response  = requests.get(fileURL, stream=True, timeout=30)
            filedata = self.__prepare_download_files(savingURL)
            for block in response.iter_content(1024):
                if not block:
                    break
                filedata.write(block)
        except requests.exceptions.RequestException as e:
            success = False
            print "Gotta error :" + str(e)
        return success

    def __write_log(self,message):
        current = datetime.now()
        self.flog.write("%s\t%s\n"%(str(current),message))
        return

    def _parsing_main_page(self):
        print "you must define parsing main page method"
        return

    def _parsing_chapter_page(self,chapterURL):
        print "you must define parsing chapter page method"
        return

    def __reload_downloaded_chapter(self):
        with open(self.downloaded_chapter_path) as fdownloaded_chapter:
            self.downloaded_chapter = fdownloaded_chapter.readlines()
        for i in range(0,len(downloaded_chapter)):
            self.downloaded_chapter[i] = self.downloaded_chapter[i].strip()
        return

    def __reload_downloaded_image():
        with open(self.downloaded_image_path) as fdownloaded_image:
            self.downloaded_images = fdownloaded_image.readlines()
        for i in range(0,len(downloaded_images)):
            self.downloaded_images[i] = self.downloaded_images[i].strip()
        return

    def __start_log(self,logfile_path):
        self.flog = file(logfile_path,"w")
        return

    def __stop_log(self):
        self.flog.close()
        return

    def __prepare_files(self,mode):
        print "preparing file"
        self.fdownloaded_chapter = file(self.downloaded_chapter_path,mode)
        self.fdownloaded_image   = file(self.downloaded_image_path,mode)
        self.ffailure            = file(self.failure_path,mode)
        return

    def __parsing_file_name_from_url(self,url):        
        spliter = url.split("/")        
        filename = spliter[len(spliter)-1].split("?")[0]
        
        if len(filename.split(".")[0]) <= 1:
            filename = "0" + filename
        
        extension = filename.split(".")[1][0:3]
        name      = filename.split(".")[0]
        
        filename = name + "." + extension            

        return filename

    def __prepare_download_folder(self,store_path,chapter_url,chapter_count):        
        spliter = chapter_url.split("/")
        chaptername = "%s-%s-%s" % (chapter_count,spliter[3],spliter[4])
        self.directory = "%s/%s" % (store_path,chaptername)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        return chaptername


    def __process_downloading(self):        
        self._parsing_main_page()
        
        downloading = True
        chapter_count = len(self.downloaded_chapter) + 1 

        for chapter in self.chapterList:
            try:
                if not downloading:
                    print "The downloading process has been stopped"
                    break

                if chapter not in self.downloaded_chapter:
                    self.__download_chapter(chapter,chapter_count)
                    chapter_count+=1
                else:
                    print "Chapter is downloaded  : %s" % chapter                      

            except (KeyboardInterrupt, SystemExit):
                downloading = False               
                                    
                self.fdownloaded_chapter.close()
                self.fdownloaded_image.close()
    
                print "You stopped the downloading process, terminating..."
        return

    def __close_all_logs(self):
        self.fdownloaded_chapter.close()
        self.fdownloaded_image.close()
        self.ffailure.close()
        return

    def __download_chapter(self,chapter,chapter_count):
        print "Getting chapter: %s" % (chapter)

        chaptername = self.__prepare_download_folder("Download",chapter,chapter_count)
                            
        self.__start_log("log/%s-log.log"%chaptername)
        self.__write_log("Getting chapter: %s" % (chapter))

        self._parsing_chapter_page(chapter)
        self.__download_chapter_images(chaptername)

        
        self.__write_log("Finished chapter : %s" % chaptername)
        self.__stop_log()        
        self.__log_downloaded_chapter(chapter)

        print "Finished chapter : %s" % chaptername
        self.downloaded_chapter.append(chapter)                    
        self.__zip_chapter()

        return

    def __zip_chapter(self):
        zipf = zipfile.ZipFile(self.directory + '.zip', 'w', zipfile.ZIP_DEFLATED)
        self.__zipdir(zipf)
        zipf.close()
        return

    def __zipdir(self,ziph):
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                ziph.write(os.path.join(root, file))
        return

    def __tar_chapter(self):
        with tarfile.open(self.directory + '.tar.gz', "w:gz") as tar:
            tar.add(self.directory, arcname=os.path.basename(self.directory))
        return

    def __download_chapter_images(self,chaptername):
        total_file = len(self.imageList)
        i = 0
        for fileURL in self.imageList:
            i+=1
            filename = self.__parsing_file_name_from_url(fileURL)

            savingURL = "%s/%s-%s" %(self.directory,i,filename)                    
            downloading_image = "%s - %s\n" % (self.directory, fileURL)
            print downloading_image

            if downloading_image not in self.downloaded_images:
                print "Downloading %s - %s - url : %s" % (chaptername,filename, fileURL)

                result = self.__download_files(fileURL,savingURL)
                if result:
                    print "Downloaded %s/%s" % (i,total_file)                 
                else:
                    print "Failed %s/%s" % (i,total_file)
                    self.__log_failed_file(chaptername,fileURL)

                self.__write_log("%s\tDownloading %s - %s - url : %s" % ("Success" if result else "Failed",chaptername,filename, fileURL))
                self.__log_downloaded_image(downloading_image)
                self.downloaded_images.append(savingURL)
            else:
                self.__write_log("Downloaded %s - %s - url : %s" % (chaptername,filename, fileURL))
                print "Image is already downloaded : %s" % (downloading_image)
        return


    def __log_failed_file(self,chapter,fileURL):
        self.ffailure.write("Failed\t\%s\t%s\n"%(chapter,fileURL))
        self.ffailure.flush()
        return

    def __log_downloaded_image(self,image):
        self.fdownloaded_image.write("%s"%image)
        self.fdownloaded_image.flush()
        return
    
    def __log_downloaded_chapter(self,chapter):
        self.fdownloaded_chapter.write("%s\n"%chapter)  
        self.fdownloaded_chapter.flush()
        return

    def start_download(self):
        print "start downloading"
        self.__prepare_files("w")
        self.__process_downloading()
        return

    def resume_download(self):
        print "resume downloading"
        self.__reload_downloaded_chapter()
        self.__reload_downloaded_image()

        self.__prepare_files("a")
                
        self.__process_downloading()
        return
