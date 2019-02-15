import time
from threading import Thread
from src.image_scraper import *
import ctypes


def convert_time_in_seconds(hours):
    return int(hours * 3600)


class RandomWallpaper:

    def __init__(self, query="Beautiful scenery", interval=1.0, ui=None):
        """

        :param query: Query to be searched
        :param interval: wallpaper changing interval (in hours)
        """
        self.ui = ui
        self.SPI_SETDESKWALLPAPER = 20
        self.query = query
        self.interval = convert_time_in_seconds(interval)
        self.timer = None
        self.toBeRun = True
        self.img_scrape = ImageScraper(self.ui)

    def start(self):
        def set_and_wait():
            while self.toBeRun:
                try:
                    self.set_random_wallpaper()
                    time.sleep(self.interval)
                except ConnectionError as ce:
                    self.ui.text.append("Please Wait for 1 minute!")
                    self.ui.wait()
                except Exception as e:
                    self.ui.text.append(e)

        self.toBeRun = True
        if self.timer is None:
            self.timer = Thread(target=set_and_wait, daemon=True)
            self.timer.start()
            self.ui.text.append("Timer started")

    def set_random_wallpaper(self):
        try:
            tmp_image = self.img_scrape.get_random_image_of(self.query)
            if tmp_image:
                ctypes.windll.user32.SystemParametersInfoW(self.SPI_SETDESKWALLPAPER, 0, tmp_image.name, 0)
                self.ui.text.append("Wallpaper set!")
                tmp_image.delete = True
        except ValueError as e:
            self.ui.text.append(e)

    def set_time_interval(self, interval):
        self.interval = convert_time_in_seconds(interval)
        self.ui.text.append("Interval set to " + str(interval))

    def set_search_query(self, query):
        self.query = query
        self.ui.text.append("Query set to " + str(query))

    def stop(self):
        if self.timer:
            self.ui.text.append("Stopping Random Wallpaper")
            self.timer = None
            self.toBeRun = False
