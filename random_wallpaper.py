import time
from threading import Timer, Thread
from sched import scheduler
from image_scraper import *
import ctypes


def convert_time_in_seconds(hours):
    return int(hours * 3600)


class RandomWallpaper:

    def __init__(self, query="Beautiful scenery", interval=1.0, text=None):
        """

        :param query: Query to be searched
        :param interval: wallpaper changing interval (in hours)
        """
        self.text = text
        self.SPI_SETDESKWALLPAPER = 20
        self.query = query
        self.interval = convert_time_in_seconds(interval)
        self.timer = None
        self.toBeRun = True
        self.img_scrape = ImageScraper(self.text)

    def start(self):
        def set_and_wait():
            while self.toBeRun:
                self.set_random_wallpaper()
                time.sleep(self.interval)
        self.toBeRun = True
        if self.timer is None:
            self.timer = Thread(target=set_and_wait)
            self.timer.start()
            self.text.append("Timer started")

    def set_random_wallpaper(self):
        tmp_image = self.img_scrape.get_random_image_of(self.query)
        if tmp_image:
            ctypes.windll.user32.SystemParametersInfoW(self.SPI_SETDESKWALLPAPER, 0, tmp_image.name, 0)
            self.text.append("Wallpaper set!")
            return tmp_image
        return None

    def set_time_interval(self, interval):
        self.interval = convert_time_in_seconds(interval)

    def set_search_query(self, query):
        self.query = query

    def stop(self):
        if self.timer:
            self.toBeRun = False
