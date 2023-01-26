from selenium.webdriver.common.by import By
from selenium import webdriver
from threading import Thread, active_count
from time import sleep
import youtube_dl


class YoutubeMusic:
    def __init__(self):
        self.BASE_URL = "https://music.youtube.com/search?q="

        self.options = webdriver.FirefoxOptions()
        self.options.headless = True

    def pull_queue(self, search_array):
        for query in search_array:
            while active_count() > 9: sleep(5)
            Thread(target=self.pull, args=(query,)).start()

    def pull(self, search):
        browser = webdriver.Firefox(options=self.options)
        url = self.get_url(search, browser)
        self.download(url)

    def get_url(self, search, browser):
        # get the page
        print("Getting URL of", search)
        browser.get(self.BASE_URL + search)

        # wait for header filters to render and click 'songs'
        sleep(3)
        header = browser.find_element(By.XPATH, '//*[@id="chips"]/*[1]')
        header.click()

        # wait for the new results to load and get the first song link (formatted)
        sleep(3)
        result = browser.find_element(By.XPATH, '//*[@id="contents"]/*[1]/div[2]/*[1]/*[1]/*[1]')
        print("Got URL for ", search)
        return result.get_attribute('href').replace('//music.y', '//www.y')

    def download(self, url):
        print('Downloading', url)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                # 'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s-%(id)s.%(ext)s',
            'quiet': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Done downloading ", url)